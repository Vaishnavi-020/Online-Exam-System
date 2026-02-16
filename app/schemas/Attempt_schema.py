from pydantic import BaseModel

class ViewAttempts(BaseModel):
    id:int
    student_id:int
    exam_id:int

    class Config:
        from_attributes=True