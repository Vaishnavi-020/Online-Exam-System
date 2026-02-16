from sqlalchemy import Table,Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

exam_question_association=Table(
    'exam_questions',Base.metadata,
    Column('exam_id',Integer,ForeignKey('exam.id'),primary_key=True),
    Column('question_id',Integer,ForeignKey('question_bank.id'),primary_key=True)
)

