from pydantic import BaseModel
from typing import List
from app.Enum.diffiulty_level_enum import DifficultyLevel

class ObjectiveQuestionCreate(BaseModel):
    difficulty_level:DifficultyLevel
    question:str
    options:List[str]
    correct_answer:str
    max_marks:int