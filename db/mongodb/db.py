import motor.motor_asyncio
import os
MONGO_DETAILS = ''
if os.environ.get('APP_LOCATION') == 'heroku':
    MONGO_DETAILS = os.getenv('MONGO_URI')
else:
    MONGO_DETAILS = os.getenv('MONGO_URI_LOCAL')
    
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client['learning-platform']

user_collection = database.get_collection('users')
enrollment_collection = database.get_collection('enrollments')
course_collection = database.get_collection('courses')
course_of_the_day_collection = database.get_collection('courses_of_the_day')
payment_collection = database.get_collection('payments')
students_view = database.get_collection('students')
lecturers_view = database.get_collection('lecturers')