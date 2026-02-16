from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas.users_schema import UserCreate,UserRead,UserResponse,Token
from app.service.authorization_service import create_user,login_user
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
from app.core.config import SECRET_KEY,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from app.models import User
from app.dependencies import get_current_user

router=APIRouter(prefix='/authorization',tags=['Authorization'])

@router.post('/register',status_code=201)
def register_user(user:UserCreate,db:Session=Depends(get_db)):
    return create_user(user,db)

@router.post('/login',response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db:Session=Depends(get_db)):
    return login_user(form_data,db)