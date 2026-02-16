from fastapi import APIRouter,Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.service.exam_service import draft_exam_service,schedule_exam_service,delete_exam_service,is_attempt_service,submit_exam_service,view_scheduled_exams_service,register_exam_service,view_attempts_service,exam_evaluation_service,result_publication_service,view_published_result_service,view_exam_questions_objective_service,update_exam_service,answer_exam_questions_service,view_all_exam_service,view_answers_service
from app.schemas.Evaluation_schema import EvaluationResponse,EvaluationIn
from app.schemas.Student_response_schema import StudentResponse,ViewAnswers
from app.schemas.Attempt_schema import ViewAttempts
from app.schemas.exam_schema import ExamDraft,ExamSchedule,ExamResponse,ExamUpdate,StudentQuestionResponseObjective,ViewExams
from typing import List

router=APIRouter(prefix='/exam',tags=['Exam'])

@router.post('/{course_id}/create_exam')
def draft_exam(course_id:int,draft_exam:ExamDraft,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return draft_exam_service(course_id,draft_exam,db,current_user)

@router.put('/{exam_id}/update')
def update_exam(exam_id:int,exam_data:ExamUpdate,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return update_exam_service(exam_id,exam_data,db,current_user)

@router.delete('/{exam_id}')
def delete_exam(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return delete_exam_service(exam_id,db,current_user)

@router.get('/all_exams',response_model=List[ViewExams])
def view_all_exams(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_all_exam_service(db,current_user)

@router.post('/{exam_id}/schedule_exam')
def schedule_exam(exam_id:int,scheduled_exam:ExamSchedule,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return schedule_exam_service(exam_id,scheduled_exam,db,current_user)

@router.get('/all_scheduled_exams',response_model=List[ExamResponse])
def get_exams(db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_scheduled_exams_service(db,current_user)

@router.post('/{exam_id}/register')
def register_exam(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return register_exam_service(exam_id,db,current_user)

@router.get('/{exam_id}/objective_questions',response_model=List[StudentQuestionResponseObjective])
def view_exam_questions_objective(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_exam_questions_objective_service(exam_id,db,current_user)

# @router.get('/{exam_id}/subjective_questions',response_model=List[StudentQuestionResponseSubjective])


@router.post('/{exam_id}/attempt')
def is_attempt(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return is_attempt_service(exam_id,db,current_user)

@router.post('/{exam_id}/{question_id}/answer')
def answer_exam_question(exam_id:int,question_id:int,response_data:StudentResponse,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return answer_exam_questions_service(exam_id,question_id,response_data,db,current_user)

@router.post('/{exam_id}/submit')
def submit_exam(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return submit_exam_service(exam_id,db,current_user)

@router.get('/{exam_id}/attempts',response_model=List[ViewAttempts])
def view_attempts(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_attempts_service(exam_id,db,current_user)

@router.get('/{exam_id}/{student_id}/{question_id}/answers',response_model=ViewAnswers)
def view_answers(exam_id:int,student_id:int,question_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_answers_service(exam_id,student_id,question_id,db,current_user)

@router.post('/{exam_id}/evaluation',response_model=EvaluationResponse)
def exam_evaluation(new_evaluation:EvaluationIn,exam_id:int,student_id:int,attempt_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return exam_evaluation_service(new_evaluation,exam_id,student_id,attempt_id,db,current_user)

@router.post('/{exam_id}/publish_result')
def result_publication(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return result_publication_service(exam_id,db,current_user)

@router.get('/{exam_id}/view_result')
def view_published_result(exam_id:int,db:Session=Depends(get_db),current_user=Depends(get_current_user)):
    return view_published_result_service(exam_id,db,current_user)