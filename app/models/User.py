from sqlalchemy import Column,Integer,String,Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.Enum.roles_enum import RoleType

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    role=Column(Enum(RoleType,name="role-type"),nullable=False)
    password_hash=Column(String,nullable=False)

    courses=relationship("Course",back_populates="faculty")
    exams=relationship("Exam",back_populates="faculty")
    attempt=relationship("Attempt",back_populates="student")
    answers=relationship("StudentAnswer",back_populates='student')