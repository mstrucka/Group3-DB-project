from datetime import datetime
from db.mongodb.db import course_collection, payment_collection, enrollment_collection
from bson.objectid import ObjectId
from db.mongodb.payment import PaymentSchema

async def create_payment(user_id, data):
    '''
        When making a payment, one or more course ids are passed (simulating that the user wants to buy one or more)
        Total price for the payment is aggregated, and a enrollments is created for each course.
    '''
    # Make sure that the user is not already enrolled in any of the desired courses
    course_ids = data['course_ids']
    course_ids = [ ObjectId(id) for id in course_ids ]
    
    async for enrollment in enrollment_collection.find({ 'student_id': ObjectId(user_id), 'course_id': { '$in': course_ids } }):
        course_id = enrollment['course_id']
        course = await course_collection.find_one({'_id': ObjectId(course_id)})
        title = course['title']
        return {'error': f'already enrolled in course "{title}"'}

    
    total_price = 0.0
    async for course in course_collection.find({'_id': { '$in': course_ids }}):
        total_price += course['price']

    data['total'] = total_price
    data['date'] = datetime.now().isoformat()
    data['is_refund'] = False
    del data['course_ids']
    
    payment = await payment_collection.insert_one(data)
    new_payment = await payment_collection.find_one({'_id': payment.inserted_id})

    # now inserting enrollments
    enrollments = []
    for id in course_ids:
        enrollment = {
            'student_id': user_id,
            'course_id': id,
            'payment_id': payment.inserted_id}
        enrollments.append(enrollment)

    await enrollment_collection.insert_many(enrollments)

    return PaymentSchema(**new_payment)
