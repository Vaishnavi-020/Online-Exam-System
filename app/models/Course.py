from sqlalchemy import Column,Integer,String,Enum,ForeignKey,UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class Course(Base):
    __tablename__="course"
    id=Column(Integer,primary_key=True)
    course_name=Column(String,nullable=False)
    faculty_id=Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=False)

    __table_args__=(
        UniqueConstraint('course_name','faculty_id',name='uq_course_faculty'),
    )
    
    exams=relationship("Exam",back_populates="course",cascade="all, delete-orphan")
    faculty=relationship("User",back_populates="courses")