from db.mongodb.db import course_collection, payment_collection, enrollment_collection, client
from bson.objectid import ObjectId
from db.sql.enrollment import EnrollmentBase

async def create_payment(user_id, data):
    '''
        When making a payment, one or more course ids are passed (simulating that the user wants to buy one or more)
        Total price for the payment is aggregated, and a enrollments is created for each course.
    '''
    course_ids = data['course_ids']
    total_price = 0.0

    for id in course_ids:
        async for course in course_collection.find({'_id': ObjectId(id)}):
            total_price += course.price

    data['total'] = total_price
    del data['course_ids']

    payment = await payment_collection.insert_one(data)
    new_payment = await payment_collection.find_one({'_id': payment.inserted_id})

    # now inserting enrollments
    enrollments = []
    for id in course_ids:
        enrollment = {'student_id': user_id, 'course_id': id, 'payment_id': payment.inserted_id}
        enrollments.append(enrollment)

    await enrollment_collection.insert_many(enrollments)

    return new_payment
