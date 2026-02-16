from pydantic import BaseModel
from typing import Optional

class StudentResponse(BaseModel):
    selected_option:Optional[int]=None
    answer_text:Optional[str]=None

class ViewAnswers(BaseModel):
    exam_id:int
    student_id:int
    question_id:int
    selected_option:Optional[int]=None
    answer_text:Optional[str]=None

    