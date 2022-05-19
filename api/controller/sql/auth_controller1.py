from fastapi import Depends, HTTPException, status
from api.models.auth import UserCreate, UserInDB, TokenData
import api.controller.sql.user_controller as user_ctrl_sql
import api.controller.mongo.user_controller as user_ctrl_mongo
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
import api.controller.sql.user_controller as user_ctrl
from db.DbTypes import DbTypes

oauth2_scheme_sql = OAuth2PasswordBearer(tokenUrl='/api/v1/sql/auth/token')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = '372c63277d2be40050086c25a2b0272e48930f0046f3f4195275b78ffc7daba0'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str):
    # authenticate user against DB
    user = get_user(email)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
    
def get_user(email: str):
    user_dict = user_ctrl_sql.get_by_email(email)
    return UserInDB(**user_dict['user'])

def get_current_user(token: str = Depends(oauth2_scheme_sql)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def register_user(user: UserCreate):
    user_dict = user.dict()
    user_dict['password_hash'] = get_password_hash(user_dict['password'])
    del user_dict['password']
    new_user = user_ctrl.create_user(user_dict)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": new_user['email']}, expires_delta=access_token_expires
    )

    return {"msg": "You have been registered", "access_token": access_token, "token_type": "bearer"}

