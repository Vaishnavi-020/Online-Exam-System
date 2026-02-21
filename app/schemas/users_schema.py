from pydantic import BaseModel,EmailStr

class UserBase(BaseModel):
    name:str
    email:EmailStr
    role:str

class UserCreate(UserBase):
    password:str

class UserRead(UserBase):
    id:int
    class Config:
        from_attributes=True

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    role:str

    class Config:
        from_attributes=True
        
# class Token(BaseModel):
#     access_token: str
#     token_type: str

class UserOut(BaseModel):
    id: int
    email: str
    role: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut