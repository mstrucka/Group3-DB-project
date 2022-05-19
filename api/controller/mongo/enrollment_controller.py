from bson.objectid import ObjectId
from db.mongodb.db import enrollment_collection
from api.models.auth import UserInDB
from db.sql.enrollment import EnrollmentBase

async def get_by_user(user_id: str):
    enrollments = []
    print(user_id)
    async for enrollment in enrollment_collection.find({'student_id': ObjectId(user_id)}):
        enrollments.append(EnrollmentBase(**enrollment))
    return enrollments