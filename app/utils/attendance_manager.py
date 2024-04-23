# Path: app/utils/attendance_manager.py
# Description: SRM Student Portal Attendance Manager API Interface.

from io import BytesIO, StringIO
from bs4 import BeautifulSoup
from PIL import Image as PILImage
import pandas as pd
import pytesseract
import httpx
import ast
import asyncio
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.logging import logger
from app.config import settings
from app.utils import models

SRM_STUDENT_PORTAL_URI = "https://sp.srmist.edu.in/srmiststudentportal/students/loginManager/youLogin.jsp"
SRM_STUDENT_PORTAL_GET_CAPTCHA_URI = "https://sp.srmist.edu.in/srmiststudentportal/captchas"
ATTENDANCE_PAGE_URI = "https://sp.srmist.edu.in/srmiststudentportal/students/report/studentAttendanceDetails.jsp"
MONTHLY_ATTENDANCE_PAGE_URI = "https://sp.srmist.edu.in/srmiststudentportal/students/report/studentAttendanceDetailsInner.jsp"
TIMETABLE_PAGE_URI = "https://sp.srmist.edu.in/srmiststudentportal/students/report/studentTimeTableDetails.jsp"

class AttendanceManager:
    """SRM Student Portal Attendance Manager API Interface."""
    def __init__(self, username: str = settings.SRM_PORTAL_USERNAME, password: str = settings.SRM_PORTAL_PASSWORD) -> None:
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
        }

    async def login(self) -> None:
        """Login to SRM Student Portal."""
        # Make GET request to SRM Student Portal
        await self.client.get(SRM_STUDENT_PORTAL_URI, headers=self.headers)

        # Get Captcha
        captcha_response = await self.client.get(
            SRM_STUDENT_PORTAL_GET_CAPTCHA_URI, headers=self.headers
        )
        captcha_text = pytesseract.image_to_string(
            PILImage.open(BytesIO(captcha_response.content))
        ).strip()

        # Login
        response = await self.client.post(
            SRM_STUDENT_PORTAL_URI,
            data={
                "txtPageAction": "1",
                "txtAN": self.username,
                "txtSK": self.password,
                "hdnCaptcha": captcha_text,
            }
        )
        
        # Check for Login Error
        if "Login Error : Invalid net id or password" in response.text:
            logger.warning(f"Invalid Username or Password")
            raise HTTPException(status_code=401, detail="Invalid Username or Password")

        # Check for Captcha Error, If so then try again
        if "Invalid Captcha...." in response.text:
            logger.warning(f"Invalid Captcha, Trying Again...")
            await self.login()
            
        # Check status code
        # status should be `302` because after successful login it redirects to another page 
        if response.status_code != 302:
            logger.error(f"Login Failed. Status Code: {response.status_code}")
            raise HTTPException(status_code=503, detail="SRM Student Portal is Down or Login Failed. Try Again Later.")
        
    async def attendance_page(self) -> BeautifulSoup:
        """Get Attendance Page."""
        # Make GET request to Attendance Page
        response = await self.client.post(ATTENDANCE_PAGE_URI, headers=self.headers)

        # Parse HTML
        attendance_page = BeautifulSoup(response.text, "html.parser")

        return attendance_page

    async def get_monthly_absent_details(self, month: str, year: str) -> list[dict[str, str | int]]:
        """Get Monthly Absent Details."""
        response = await self.client.post(
            MONTHLY_ATTENDANCE_PAGE_URI,
            data={
                "ids": 1,
                "attendanceMonth": month,
                "attendanceYear": year,
            },
        )
        absent_details = pd.read_html(StringIO(str(response.text)))[0]
        return ast.literal_eval(absent_details.to_json(orient="records"))

    async def get_attendance_details(self) -> list[dict[str, str | int]]:
        """Get main Attendance Table."""
        attendance_page = await self.attendance_page()

        # Get Attendance Table
        attendance_table = attendance_page.find_all("table", class_="table")[0]

        # Convert to DataFrame
        attendance_df = pd.read_html(StringIO(str(attendance_table)))[0]

        # Remove Unwanted Subject Codes
        blacklist_codes = ["CL", "Total"]
        attendance_df = attendance_df[~attendance_df["Code"].isin(blacklist_codes)]

        """Get Absent Details for every month."""

        # Get Cumulative Attendance Table
        cumulative_attendance_table = attendance_page.find_all("table", class_="table")[
            1
        ]
        cumulative_attendance_df = pd.read_html(
            StringIO(str(cumulative_attendance_table))
        )[0]
        month_map = {
            "JAN": 1,
            "FEB": 2,
            "MAR": 3,
            "APR": 4,
            "MAY": 5,
            "JUN": 6,
            "JUL": 7,
            "AUG": 8,
            "SEP": 9,
            "OCT": 10,
            "NOV": 11,
            "DEC": 12,
        }

        month_year = []
        for _, row in cumulative_attendance_df.iterrows():
            mon, year = row["Month / Year"].split(" / ")
            month_year.append((month_map[mon], year))

        # run `get_monthly_absent_details` for every month and year parallelly
        daywise_absent_details = await asyncio.gather(
            *[
                self.get_monthly_absent_details(month, year)
                for month, year in month_year
            ]
        )
        daywise_absent_details = [
            item for sublist in daywise_absent_details for item in sublist
        ]

        return (
            ast.literal_eval(attendance_df.to_json(orient="records")),
            daywise_absent_details,
        )

