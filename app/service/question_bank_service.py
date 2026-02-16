from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User,Question,Course,Exam
from app.Enum.question_type_enum import QuestionType
from app.Enum.exam_status_enum import ExamStatus
from .system_driven import sync_exam_status
from sqlalchemy.exc import IntegrityError

def create_questions_service(
    course_id: int,
    db: Session,
    current_user: User,
    question_type: QuestionType,
    payload
):
    if current_user.role != "faculty":
        raise HTTPException(403, "Only faculty allowed")

    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(404, "Course does not exist")
    print(course.faculty_id)
    print(current_user.id)
    if course.faculty_id!=current_user.id:
        raise HTTPException(403,"You are not assigned to this course")
   

    if question_type == QuestionType.objective:
        if not payload.options or len(payload.options)<=1:
            raise HTTPException(400,"Options should be more than one")
        if not payload.options or not payload.correct_answer:
            raise HTTPException(400, "Options and correct answer required")
        if payload.correct_answer not in payload.options:
            raise HTTPException(400, "Correct answer must be in options")
        if payload.max_marks is None or payload.max_marks <= 0:
            raise HTTPException(400, "Max marks must be > 0")

    if question_type == QuestionType.subjective:
        if payload.max_marks is None or payload.max_marks <= 0:
            raise HTTPException(400, "Max marks must be > 0")

    question = Question(
        course_id=course_id,
        created_by_faculty_id=current_user.id,
        question_type=question_type,
        difficulty_level=payload.difficulty_level,
        question=payload.question,
        options=getattr(payload, "options", None),
        correct_answer=getattr(payload, "correct_answer", None),
        max_marks=getattr(payload, "max_marks", None),
    )

    db.add(question)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="This question already exists in this course"
        )
    db.refresh(question)

    return {
        "message": "Question created successfully",
        "question_id": question.id,
        "question_type": question_type
    }

def available_questions_service(db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty can view questions")
    return db.query(Question).filter(
            Question.created_by_faculty_id == current_user.id
            ).all()

