from sqlalchemy import Column,Integer,String,Enum,Text,ForeignKey,JSON,DateTime,UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import func

class StudentAnswer(Base):
    __tablename__="student_response"
    id=Column(Integer,primary_key=True)
    exam_id=Column(Integer,ForeignKey('exam.id',ondelete='CASCADE'),nullable=False)
    student_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    question_id=Column(Integer,ForeignKey('question_bank.id',ondelete='CASCADE'),nullable=False)
    selected_option=Column(Integer,nullable=True)
    answer_text=Column(String,nullable=True)
    saved_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    __table_args__=(
       UniqueConstraint('student_id','question_id','exam_id',name='uq_student_exam_question'),
    )

    exam=relationship("Exam",back_populates='answers')
    student=relationship("User",back_populates='answers')
    question=relationship("Question",back_populates='answer')