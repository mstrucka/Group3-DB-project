from fastapi import Depends, HTTPException, status
from api.models.auth import TokenData
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from api.controller.neo import student_controller, teacher_controller

from db.neo4jdb.user import UserCreate

oauth2_scheme_sql = OAuth2PasswordBearer(tokenUrl='/api/v1/neo4j/auth/token')
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
    if not verify_password(password, user['password_hash']):
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


def get_pw_hash_from_database(email):
    password_hash = student_controller.get_password_hash_by_email(email)
    if password_hash is None:
        password_hash = teacher_controller.get_password_hash_by_email(email)
    return password_hash


def get_user(email: str):
    user = student_controller.get_by_email(email)
    if user is None:
        user = teacher_controller.get_by_email(email)
    return user


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
    user.password = get_password_hash(user.password)
    if user.isStudent:
        student_controller.create_student(user)
    else:
        teacher_controller.create_teacher(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"msg": "You have been registered", "access_token": access_token, "token_type": "bearer"}
