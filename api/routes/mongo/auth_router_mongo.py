from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import timedelta
from api.models.auth import Token, User, UserCreate
from api.controller.mongo.auth_controller import authenticate_user, create_access_token, get_current_user, register_user, oauth2_scheme_nosql, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(
    prefix='/auth',
    tags=['Mongo Authentication'],
)

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # authenticate user against DB
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/')
def index(token: str = Depends(oauth2_scheme_nosql)):
    return {'token': token}

@router.post('/register')
async def register(user_data: UserCreate):
    res = await register_user(user_data)
    return res