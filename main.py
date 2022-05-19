from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from api.routes.sql import *
from api.routes.mongo import *
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

sql_app.include_router(auth_router1.router)
sql_app.include_router(course_router.router)
sql_app.include_router(lecture_router.router)
sql_app.include_router(enrollment_router.router)
sql_app.include_router(resource_router.router)
sql_app.include_router(user_router.router)
sql_app.include_router(payment_router.router)

mongo_app.include_router(course_router_mongo.router)
mongo_app.include_router(user_router_mongo.router)
mongo_app.include_router(auth_router_mongo.router)
mongo_app.include_router(payment_router_mongo.router)

app.mount('/api/v1/nosql', app=mongo_app, name='Mongo app')
app.mount('/api/v1/sql', app=sql_app, name='SQL app')
