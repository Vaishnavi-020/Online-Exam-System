from sqlalchemy import Column,Integer,String,Enum,Text,ForeignKey,JSON,UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base
from app.models.exam_question_association import exam_question_association
from app.Enum.question_type_enum import QuestionType
from app.Enum.diffiulty_level_enum import DifficultyLevel

class Question(Base):
    __tablename__="question_bank"
    id=Column(Integer,primary_key=True)
    created_by_faculty_id=Column(Integer,ForeignKey('users.id',ondelete='SET NULL'))
    course_id=Column(Integer,ForeignKey('course.id',ondelete='CASCADE'),nullable=False)
    question_type=Column(Enum(QuestionType,name='question_type'),nullable=False,default=QuestionType.objective)
    difficulty_level=Column(Enum(DifficultyLevel,name='difficulty_level'),nullable=False,default=DifficultyLevel.easy)
    question=Column(Text,nullable=False)
    options=Column(JSON,nullable=True)
    correct_answer=Column(Text,nullable=True)
    max_marks=Column(Integer)

    __table_args__=(UniqueConstraint(
        'course_id','question',name='uq_course_question'
    ),)


    exam=relationship("Exam",secondary=exam_question_association,back_populates="questions")
    answer=relationship("StudentAnswer",back_populates='question')