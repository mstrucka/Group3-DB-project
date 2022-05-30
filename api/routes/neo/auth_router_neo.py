from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from api.models.auth import Token, User
from api.controller.neo.auth_controller_neo import authenticate_user, create_access_token, get_current_user, register_user, oauth2_scheme_sql, ACCESS_TOKEN_EXPIRE_MINUTES
from db.neo4jdb.user import UserCreate

router = APIRouter(
    prefix='/auth',
    tags=['NEO4J Authentication'],
)


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/')
def index(token: str = Depends(oauth2_scheme_sql)):
    return {'token': token}


@router.post('/register')
def register(user_data: UserCreate):
    return register_user(user_data)