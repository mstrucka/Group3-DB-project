
from pprint import pprint
from api.routes.mongo.CourseAvgPrice import CourseAvgPrice
from db.mongodb.db import course_collection, course_of_the_day_collection
from db.mongodb.course import CourseSchema
from bson.objectid import ObjectId

async def get_all_courses() -> list:
    courses = []
    async for course in course_collection.find():
        courses.append(CourseSchema(**course))
    return courses

async def get_course_of_the_day() -> dict:
    cursor = course_of_the_day_collection.find().sort('date', -1).limit(1)
    course_of_the_day = await cursor.to_list(length=1)
    
    course_id = course_of_the_day[0]['course_id']
    # now get the course
    course_of_the_day = await course_collection.find_one({'_id': ObjectId(course_id)})
    return CourseSchema(**course_of_the_day)

async def get_course_by_id(id: str) -> dict:
    course = await course_collection.find_one({'_id': ObjectId(id)})
    return course

async def delete_course_by_id(id: str) -> bool:
    course = await course_collection.find_one({'_id': ObjectId(id)})
    if course:
        await course_collection.delete_one({'_id': ObjectId(id)})
        return True
    return False

async def edit_course(id: str, data: dict) -> bool | dict:
    if len(data) < 1:
        return False
    course = await course_collection.find_one({'_id': ObjectId(id)})
    if course:
        updated_course = await course_collection.update_one(
            {'_id': ObjectId(id)}, {'$set': data}
        )
        if updated_course:
            res = await course_collection.find_one({'_id': ObjectId(id)})
            return res
        return False

async def create_course(data: dict) -> dict:
    course = await course_collection.insert_one(data)
    new_course = await course_collection.find_one({'_id': course.inserted_id})
    return new_course

async def search_courses(query: str, limit: int) -> list:
    courses = course_collection.find(
        {'$text': {'$search': query}}, {'score': {'$meta': 'textScore'} }
    )
    c = await courses.to_list(length=limit)
    c = sorted(c, key=lambda x: x['score'], reverse=True)
    c = [ CourseSchema(**el) for el in c ]
    return c

async def get_avg_price_by_lecturer():
    pipeline = [
        {
            '$group': {
                '_id': '$lecturer_id',
                'avg_price': {
                    '$avg': '$price'
                }
            },
        },
    ]
    res = await course_collection.aggregate(pipeline).to_list(length=None)
    res = [ CourseAvgPrice(**el) for el in res ]
    return res