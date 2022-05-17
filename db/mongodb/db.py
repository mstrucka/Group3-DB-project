import motor.motor_asyncio
import os
MONGO_DETAILS = os.getenv('MONGO_URI')
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client['learning-platform']

user_collection = database.get_collection('users')
enrollment_collection = database.get_collection('enrollments')
course_collection = database.get_collection('courses')
payment_collection = database.get_collection('payments')