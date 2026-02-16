from fastapi import HTTPException,status
from passlib.context import CryptContext
from jose import jwt,JWTError
from app.core.config import SECRET_KEY,JWT_ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime,timedelta

pwd_cxt=CryptContext(schemes=["bcrypt"],deprecated="auto")

class Hash():
    def bcrypt(password: str):
        return pwd_cxt.hash(password)

pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password,hash):
    return pwd_context.verify(password,hash)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
        )