from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from api.routes import *

import logging
log = logging.basicConfig(
    level=logging.DEBUG, 
    filename='app.log', 
    filemode='a+', 
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
)

app = FastAPI(debug=True, description='DB for devs project. Get rect')

api_app = FastAPI(debug=True, description='API app (might be different app per db type..)')

api_app.include_router(auth_router1.router)
api_app.include_router(course_router.router, prefix='/{db}')
api_app.include_router(lecture_router.router, prefix='/{db}')
api_app.include_router(enrollment_router.router, prefix='/{db}')
api_app.include_router(resource_router.router, prefix='/{db}')
api_app.include_router(user_router.router, prefix='/{db}')
api_app.include_router(payment_router.router, prefix='/{db}')

app.mount('/api/v1', app=api_app, name='API app')
