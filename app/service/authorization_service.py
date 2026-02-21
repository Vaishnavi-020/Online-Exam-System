from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from app.models import User
from app.schemas.users_schema import UserCreate,UserRead,UserResponse
from app.core.security import hash_password,verify_password,create_access_token
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import SECRET_KEY,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES

def create_user(user:UserCreate,db:Session):
    existing_user=db.query(User).filter(User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail="User with this email already exists")
    user=User(name=user.name,
              email=user.email,
              role=user.role,
              password_hash=hash_password(user.password))
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message":"User registered successfully"}

def login_user(form_data:OAuth2PasswordRequestForm,
               db:Session):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
    data={
        "sub": str(user.id),
        "role": user.role  
    },
    expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user":{
            "id":user.id,
            "email":user.email,
            "role":user.role
        }
    }