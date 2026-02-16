from sqlalchemy import Column,Integer,String,Enum,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base
from sqlalchemy import func
from app.models.exam_question_association import exam_question_association
from app.Enum.exam_status_enum import ExamStatus
from app.Enum.diffiulty_level_enum import DifficultyLevel
from app.Enum.exam_type_enum import ExamType
# def two_days_from_now():
#     return datetime.now() + timedelta(days=2)

class Exam(Base):
    __tablename__="exam"
    id=Column(Integer,primary_key=True)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)

    exam_status=Column(Enum(ExamStatus,name='exam_status'),nullable=False,default=ExamStatus.draft)

    start_date=Column(DateTime(timezone=True),nullable=True)
    duration_minutes=Column(Integer,nullable=True)

    difficulty_level=Column(Enum(DifficultyLevel,name='difficulty_level'),
                            nullable=False,
                            default=DifficultyLevel.easy)
    exam_type=Column(Enum(ExamType,name='exam_type'),
                     nullable=False,
                     default=ExamType.objective)
    total_marks=Column(Integer)

    faculty_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    course_id=Column(Integer,ForeignKey('course.id',ondelete='CASCADE'),nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())

        # Relationships
    questions = relationship(
        "Question",
        secondary=exam_question_association,
        back_populates="exam"
    )

    faculty = relationship("User", back_populates="exams")

    attempts = relationship(
        "Attempt",
        back_populates="exam",
        cascade="all, delete-orphan"
    )

    course = relationship("Course", back_populates="exams")

    answers=relationship("StudentAnswer",back_populates="exam")
