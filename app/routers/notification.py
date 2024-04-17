# @app.post("/notifications/unread")
# async def get_unread_notifications(username: str = Form(default="")):
#     """Get Notifications."""
#     # Check Username
#     if not username:
#         raise HTTPException(
#             status_code=400, detail="username is required form parameter"
#         )

#     # Check if User Exists in Database
#     db = Database()
#     if username not in [user for user, _ in db.get_all_users()]:
#         raise HTTPException(
#             status_code=400, detail=f"{username}: User Not registered for Notifications"
#         )

#     return Notifications().retrieve_unread_notifications(username)


# @app.post("/notifications/all")
# async def get_all_notifications(username: str = Form(default="")):
#     """Get Notifications."""
#     # Check Username
#     if not username:
#         raise HTTPException(
#             status_code=400, detail="username is required form parameter"
#         )

#     # Check if User Exists in Database
#     db = Database()
#     if username not in [user for user, _ in db.get_all_users()]:
#         raise HTTPException(
#             status_code=400, detail=f"{username}: User Not registered for Notifications"
#         )

#     return Notifications().retrieve_all_notifications(username)
