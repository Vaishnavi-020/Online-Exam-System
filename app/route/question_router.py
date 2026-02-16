from fastapi import APIRouter,Depends,Body
from app.database import get_db
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.service.question_bank_service import create_questions_service,available_questions_service
from app.service.exam_service import add_question_to_draft_service,remove_questions_from_draft_service
from app.schemas.question_objective_schema import ObjectiveQuestionCreate
from app.schemas.question_subjective_schema import SubjectiveQuestionCreate
from app.schemas.AddQuestion_schema import ExamAddQuestion

router=APIRouter(prefix='/question_bank',tags=['Question_Bank'])

@router.post("/{course_id}/questions/objective")
def create_objective_question(
    course_id:int,
    payload: ObjectiveQuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_questions_service(
        course_id=course_id,
        db=db,
        current_user=current_user,
        question_type="objective",
        payload=payload
    )

@router.post("/{course_id}/questions/subjective")
def create_subjective_question(
    course_id:int,
    payload: SubjectiveQuestionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_questions_service(
        course_id=course_id,
        db=db,
        current_user=current_user,
        question_type="subjective",
        payload=payload
    )

@router.get('/all_questions')
def available_questions(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return available_questions_service(db,current_user)

@router.post('/add_questions')
def add_question_to_draft(exam_id:int,data:ExamAddQuestion,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return add_question_to_draft_service(exam_id,data,db,current_user)

@router.delete('/{exam_id}/{question_id}')
def remove_questions_from_draft(exam_id:int,question_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return remove_questions_from_draft_service(exam_id,question_id,db,current_user)

