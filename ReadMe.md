# SRM Student Portal Attendance Manager API 🎓📊

Welcome to the SRM Student Portal Attendance Manager API! This API provides endpoints to access attendance details, timetable, and notifications for SRM Institute of Science and Technology students.

## Endpoints 🚀

### 1. Get Attendance Details

- **URL:** `/get_attendance_details`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
  - `password`: SRM Student Portal password
- **Description:** Retrieves course-wise attendance details and monthly attendance summary for the specified user.
- **Response:**
  - `CourseWiseAttendance`: Course-wise attendance details
  - `MonthlyAttendance`: Monthly attendance summary

### 2. Get Timetable

- **URL:** `/get_timetable`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
  - `password`: SRM Student Portal password
- **Description:** Retrieves the timetable for the specified user.
- **Response:** Timetable for the user.

### 3. Register User for Notifications

- **URL:** `/notifications/register`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
  - `password`: SRM Student Portal password
- **Description:** Registers the user for attendance notifications.
- **Response:** Status of registration.

### 4. Unregister User from Notifications

- **URL:** `/notifications/unregister`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
- **Description:** Unregisters the user from attendance notifications.
- **Response:** Status of unregistration.

### 5. Get Unread Notifications

- **URL:** `/notifications/unread`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
- **Description:** Retrieves unread notifications for the specified user and marks them as read.
- **Response:** List of unread notifications.

### 6. Get All Notifications

- **URL:** `/notifications/all`
- **Method:** POST
- **Parameters:**
  - `username`: SRM Student Portal username (6 characters)
- **Description:** Retrieves all notifications for the specified user.
- **Response:** List of all notifications.

## How to Use ℹ️

1. **Register for Notifications:** Use the `/notifications/register` endpoint to register for attendance notifications by providing your SRM Student Portal username and password.
2. **Access Attendance Details:** Utilize the `/get_attendance_details` endpoint to fetch your course-wise attendance details and monthly attendance summary.
3. **View Timetable:** Retrieve your timetable using the `/get_timetable` endpoint.
4. **Check Notifications:** Check your unread notifications with the `/notifications/unread` endpoint, and view all notifications with the `/notifications/all` endpoint.
5. **Unregister from Notifications:** If you no longer wish to receive notifications, use the `/notifications/unregister` endpoint.

## Technologies Used 🛠️

- Python
- FastAPI
- Docker
- PostgreSQL
- MongoDB
- Beautiful Soup
- Pytesseract
- Pandas

## Deployment 🚢

This API can be deployed locally or on a server using Docker. Follow the provided Dockerfile and docker-compose.yml files to build and run the containerized application.

## Credits 🙌

This project was developed by [Devasheesh Mishra](https://github.com/devasheeshG/ "Github Profile"), [Aarush Dwivedi](https://github.com/XEREXUS/ "Github Profile") [Dhruv Singh Poniya](https://github.com/Dhruv-Singh-Poniya/ "Github Profile"). If you have any questions or suggestions, feel free to reach out.

---

Happy coding! 🚀📚
