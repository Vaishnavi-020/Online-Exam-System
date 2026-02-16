from pydantic import BaseModel

class EvaluationIn(BaseModel):
    marks_scored:int
    remarks:str

class EvaluationResponse(BaseModel):
    id:int
    exam_id:int
    student_id:int
    marks_scored:int
    remarks:str

    class Config:
        from_attributes=True