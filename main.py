from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from api.routes.sql import *
from api.routes.mongo import *
from api.routes.neo import *

import logging

log = logging.basicConfig(
    level=logging.DEBUG, 
    filename='app.log', 
    filemode='a+', 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
)

app = FastAPI(debug=True, description='DB for devs project. Get rect')

sql_app = FastAPI(debug=True, description='SQL app (might be different app per db type..)')
mongo_app = FastAPI(debug=True, description='Mongo DB app')
neo4j_app = FastAPI(debug=True, description='Neo4j app')

sql_app.include_router(auth_router1.router)
sql_app.include_router(course_router.router)
sql_app.include_router(lecture_router.router)
sql_app.include_router(enrollment_router.router)
sql_app.include_router(resource_router.router)
sql_app.include_router(user_router.router)
sql_app.include_router(payment_router.router)


mongo_app.include_router(course_router_mongo.router)
mongo_app.include_router(user_router_mongo.router)
mongo_app.include_router(student_router_mongo.router)
mongo_app.include_router(lecturer_router_mongo.router)
mongo_app.include_router(auth_router_mongo.router)
mongo_app.include_router(payment_router_mongo.router)

# TODO: add all the routes when finished
neo4j_app.include_router(course_router_neo.router)
neo4j_app.include_router(lecture_router_neo.router)
neo4j_app.include_router(student_router_neo.router)
neo4j_app.include_router(teacher_router_neo.router)
neo4j_app.include_router(resource_router_neo.router)
neo4j_app.include_router(payment_router_neo.router)
neo4j_app.include_router(auth_router_neo.router)

app.mount('/api/v1/mysql', app=sql_app, name='SQL app')
app.mount('/api/v1/mongo', app=mongo_app, name='Mongo app')
app.mount('/api/v1/neo4j', app=neo4j_app, name='Neo4j app')
