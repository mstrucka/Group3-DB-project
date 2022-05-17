from bson.objectid import ObjectId
from db.mongodb.db import user_collection
from api.models.auth import UserInDB, User

async def get_all_users():
    users = []
    async for user in user_collection.find():
        print(UserInDB(**user))
        x = UserInDB(**user)
        users.append(x)
        #users.append(UserInDB(**user))
    return users

async def get_user_by_id(id: str) -> dict:
    user = await user_collection.find_one({'_id': ObjectId(id)})
    return user

async def get_user_by_email(email: str):
    user = await user_collection.find_one({'email': email})
    return user

async def create_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({'_id': user.inserted_id})
    return new_user

async def delete_by_id(id: str):
    user = await user_collection.find_one({'_id': ObjectId(id)})
    if user:
        await user_collection.delete_one({'_id': ObjectId(id)})
        return True

async def edit_user(id: str, data: dict):
    if len(data) < 1:
        return {'msg': 'Need at least one property to change'}
    user = await user_collection.find_one({'_id': ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {'_id': ObjectId(id)}, {'$set': data}
        )
        if updated_user:
            return {'msg': 'User was updated'}
        return {'msg': 'User update failed'}