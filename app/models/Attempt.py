from sqlalchemy import Column,Integer,String,ForeignKey,UniqueConstraint,DateTime,Enum,Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.Enum.attempt_status_enum import AttemptStatus

class Attempt(Base):
    __tablename__="attempt"
    id=Column(Integer,primary_key=True)
    student_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    attempt_status=Column(Enum(AttemptStatus,name="attempt_status"),nullable=False,default=AttemptStatus.pending)
    exam_id=Column(Integer,ForeignKey('exam.id',ondelete='CASCADE'),nullable=False)
    started_at=Column(DateTime(timezone=True),nullable=True)
    submitted_at=Column(DateTime(timezone=True))
    auto_submitted=Column(Boolean,nullable=True)

    __table_args__=(
        UniqueConstraint('student_id','exam_id',name='uq_student_exam_enrollment'),
    )

    exam=relationship("Exam",back_populates="attempts")
    student=relationship("User",back_populates="attempt")
    evaluation=relationship("Evaluation",back_populates="attempt",uselist=False,cascade="all, delete-orphan")