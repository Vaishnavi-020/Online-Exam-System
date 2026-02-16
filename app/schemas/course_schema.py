from pydantic import BaseModel

class CourseCreate(BaseModel):
    course_name:str

class CourseOut(BaseModel):
    id:int
    course_name:str
    faculty_id:int

    class Config:
        from_attributes=True