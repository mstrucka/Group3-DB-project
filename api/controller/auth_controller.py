import os
import jwt
import time
import logging
import api.controller.user_controller as user_ctrl
from db.sql.user import User
from db.sql.sql import Session
from sqlalchemy import select
from bottle import route, get, post, put, auth_basic, request, abort, BottleException
from passlib.hash import bcrypt

jwt_secret = os.environ.get('jwt_secret')
jwt_expireoffset = int(os.environ.get('jwt_expireoffset'))
jwt_algorithm = os.environ.get('jwt_algorithm')
class AuthorizationError(BottleException):
    """ Base class for exceptions used by bottle """
    pass

def jwt_token_from_header():
    auth = request.get_header('Authorization')
    if not auth:
        raise AuthorizationError({'code': 'authorization_header_missing', 'description': 'Authorization header is expected'})
 
    parts = auth.split()
 
    if parts[0].lower() != 'bearer':
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must start with Bearer'})
    elif len(parts) == 1:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Token not found'})
    elif len(parts) > 2:
        raise AuthorizationError({'code': 'invalid_header', 'description': 'Authorization header must be Bearer + \s + token'})
 
    return parts[1]

def requires_auth(f):
    """Provides JWT based authentication for any decorated function assuming credentials available in an "Authorization" header"""
    def decorated(*args, **kwargs):
        try:
            token = jwt_token_from_header()
        except AuthorizationError as reason:
            abort(400, reason)
 
        try:
            token_decoded = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])    # throw away value
        except jwt.exceptions.ExpiredSignatureError:
            abort(401, {'code': 'token_expired', 'description': 'token is expired'})
        except jwt.exceptions.DecodeError as err:
            abort(401, {'code': 'token_invalid', 'description': err.args})
 
        return f(*args, **kwargs)
 
    return decorated
 
def build_profile(credentials):
    return { 
        'user': credentials['user'],
        'exp': time.time()+jwt_expireoffset }
 
def authenticate():
    # extract credentials from the request
    credentials = request.json
    if not credentials or 'user' not in credentials or 'password' not in credentials:
        abort(400, 'Missing or bad credentials')
 
    # authenticate against db
    try:
        user = authenticate_user(credentials)
        credentials['user'] = user
    except Exception as error_message:
        logging.exception("Authentication failure")
        abort(403, f'''Authentication failed for {credentials['user']}: {error_message}''')
 
    token = jwt.encode(build_profile(credentials), jwt_secret, algorithm=jwt_algorithm)
 
    logging.info(f'''Authentication successful for user_id={credentials['user']['id']}''')
    return { 'token': token }

def get_jwt_credentials():
    # get and decode the current token
    token = jwt_token_from_header()
    credentials = jwt.decode(token, jwt_secret, algorithms=[jwt_algorithm])
    return credentials

def authenticate_user(credentials):
    user, password = credentials.values()
    with Session() as session:
        stmt = select(User).where(User.email == user)
        res = session.execute(stmt).scalars().one()
        pass_verified = bcrypt.verify(password, res.password_hash)
        user = res.to_dict(rules=('-password_hash',))

    if pass_verified: return user
    else: raise Exception('Wrong password')

def register(values):
    if (len(values.keys()) < 6):
        return {
            'message': 'Missing required info. Firstname, lastname, date of birth, email, password and is_student must be provided'
        }

    values['password_hash'] = bcrypt.hash(values['password'])
    del values['password']
    new_user = user_ctrl.create_user(values)
    return { 'message': 'you have been registered', 'user': new_user }