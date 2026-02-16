from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.schemas.course_schema import CourseCreate,CourseOut
from app.service.course_service import new_course_service,view_all_courses_service,delete_course_service
from typing import List

router=APIRouter(prefix='/course',tags=['Course'])

@router.post('/create_course',response_model=CourseOut)
def new_course(course:CourseCreate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return new_course_service(course,db,current_user)

@router.get('/all_courses',response_model=List[CourseOut])
def view_all_courses(db:Session=Depends(get_db)):
    return view_all_courses_service(db)

@router.delete('/{course_id}')
def delete_course(course_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_course_service(course_id,db,current_user)


