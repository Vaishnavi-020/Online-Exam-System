from pydantic import BaseModel
from app.Enum.diffiulty_level_enum import DifficultyLevel

class SubjectiveQuestionCreate(BaseModel):
    difficulty_level:DifficultyLevel
    question:str
    max_marks:int