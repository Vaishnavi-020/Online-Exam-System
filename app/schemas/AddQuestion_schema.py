from pydantic import BaseModel
from typing import List

class ExamAddQuestion(BaseModel):
    question_ids:List[int]