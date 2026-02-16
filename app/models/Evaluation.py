from sqlalchemy import Column,Integer,String,Enum,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Evaluation(Base):
    __tablename__="evaluation"
    id=Column(Integer,primary_key=True)
    exam_id=Column(Integer,ForeignKey('exam.id'),nullable=False)
    student_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    attempt_id=Column(Integer,ForeignKey('attempt.id',ondelete='CASCADE'),unique=True,nullable=False)
    marks_scored=Column(Integer,nullable=False)
    remarks=Column(String)
    
    attempt=relationship("Attempt",back_populates="evaluation")