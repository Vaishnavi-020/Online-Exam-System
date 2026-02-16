from fastapi import HTTPException,Depends,status
from sqlalchemy.orm import Session
from app.models import User,Course
from app.schemas.course_schema import CourseCreate

def new_course_service(course:CourseCreate,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(status_code=403,
                            detail="Only faculty can create courses")
    existing_course=db.query(Course).filter(Course.course_name==course.course_name,Course.faculty_id==current_user.id).first()
    if existing_course:
        raise HTTPException(400,"Course already exists")
    new_course=Course(course_name=course.course_name,
                  faculty_id=current_user.id)
        
    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

def view_all_courses_service(db:Session):
    return db.query(Course).all()

def delete_course_service(course_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(status_code=403,
                            detail="Not allowed for this action")
    existing_course=db.query(Course).filter(Course.id==course_id).first()
    if not existing_course:
        raise HTTPException(status_code=404,
                            detail="Course does not exist")
    if current_user.id!=existing_course.faculty_id:
        raise HTTPException(status_code=403,
                            detail="Only faculty who created this course can perform this action")
    db.delete(existing_course)
    db.commit()
    return {"message":"Course deleted successfully"}
    