from pydantic import BaseModel
from app.Enum.exam_status_enum import ExamStatus
from app.Enum.diffiulty_level_enum import DifficultyLevel
from app.Enum.exam_type_enum import ExamType
from datetime import datetime
from typing import Optional,List

class ExamDraft(BaseModel):
    title:str
    description:Optional[str]=None
    difficulty_level:Optional[DifficultyLevel]=None
    exam_type:Optional[ExamType]=None

    class Config:
        from_attributes=True

class ViewExams(ExamDraft):
    id:int
    exam_status:ExamStatus
    total_marks:int

class ExamSchedule(BaseModel):
    start_date:datetime
    duration_minutes:int

    class Config:
        from_attributes=True

class ExamResponse(BaseModel):
    id:int
    title:str
    description:str
    difficulty_level:DifficultyLevel
    exam_type:ExamType
    exam_status:ExamStatus
    course_id:int
    start_date:datetime
    duration_minutes:int
    total_marks:int
    
    class Config:
        from_attributes=True


class ExamUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    difficulty_level: Optional[DifficultyLevel] = None

class StudentQuestionResponseObjective(BaseModel):
    id:int
    question:str
    options:Optional[List[str]]
    
    class Config:
        from_attributes=True

# class StudentQuestionResponseSubjective(BaseModel):
#     id:int
#     question:str

#     class Config:
#         from_attribute=True