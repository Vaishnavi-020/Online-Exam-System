from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import User,Exam,Attempt,Evaluation,Question,Course,exam_question_association,StudentAnswer
from app.schemas.exam_schema import ExamDraft,ExamSchedule,ExamUpdate
from app.schemas.Evaluation_schema import EvaluationIn
from app.schemas.AddQuestion_schema import ExamAddQuestion
from app.schemas.Student_response_schema import StudentResponse
from sqlalchemy import and_
from app.Enum.attempt_status_enum import AttemptStatus
from app.Enum.exam_status_enum import ExamStatus
from .system_driven import sync_exam_status
from datetime import datetime,timezone,timedelta
#Faculty => Exam setup phase

def draft_exam_service(course_id:int,draft_exam:ExamDraft,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(status_code=403,
                            detail="Only faculty can create exams")
    course=db.query(Course).filter(Course.id==course_id).first()
    if not course:
        raise HTTPException(404,'Course not found')
    if course.faculty_id!=current_user.id:
        raise HTTPException(403,"You are not allowed to create exam for this course")
    new_exam=Exam(
              title=draft_exam.title,
              description=draft_exam.description,
              difficulty_level=draft_exam.difficulty_level,
              exam_type=draft_exam.exam_type,
              course_id=course_id,
              faculty_id=current_user.id)
    
    
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    return new_exam
def add_question_to_draft_service(exam_id:int,data:ExamAddQuestion,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty can perform this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam must exist")
    if exam.faculty_id!=current_user.id:
        raise HTTPException(403,'Only faculty who created this exam can perform this action')
    if exam.exam_status!=ExamStatus.draft:
        raise HTTPException(400,"Only draft exams can add questions")
    unique_ids = set(data.question_ids)

    questions = db.query(Question).filter(
    Question.id.in_(unique_ids),
    Question.course_id == exam.course_id,
    Question.created_by_faculty_id == current_user.id,
    Question.question_type==exam.exam_type
    ).all()

    if len(questions) != len(unique_ids):
        raise HTTPException(400, "One or more questions are invalid or unauthorized")
    for q in questions:
        if q.course_id!=exam.course_id:
            raise HTTPException(400,"All questions must belong to the same course as the exam")
        if q.created_by_faculty_id!=current_user.id:
            raise HTTPException(403,"You have not created this question")
    existing_ids={q.id for q in exam.questions}
    new_question=[q for q in questions if q.id not in existing_ids]

    if not new_question:
        raise HTTPException(400,"Question already added")
    exam.questions.extend(new_question)
    db.commit()
    db.refresh(exam)

    return exam

def remove_questions_from_draft_service(exam_id:int,question_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty can perform this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    if exam.faculty_id!=current_user.id:
        raise HTTPException(403,"Only faculty who created this exam can perform this action")
    question=db.query(Question).filter(Question.id==question_id).first()
    if not question:
        raise HTTPException(404,"Question does not exist")
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.draft:
        raise HTTPException(400,"Only draft exams can be modified")
     
    if question in exam.questions:
        exam.questions.remove(question)
    else:
        raise HTTPException(400, "Question not linked to this exam")

    db.commit()

    return {"message":"Question removed successfully"}

def update_exam_service(exam_id:int,exam_data:ExamUpdate,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty is allowed to perform this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(400,"Exam not found")
    if exam.faculty_id!=current_user.id:
        raise HTTPException(403,'Not allowed to edit this exam')
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.draft:
        raise HTTPException(400,"Only draft exams can be edited")
    update_data=exam_data.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(400,"No fields provided for update")
    for field,value in update_data.items():
        setattr(exam,field,value)
        
    db.commit()
    db.refresh(exam)
    return exam
    

def delete_exam_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(status_code=403,
                            detail="Not allowed for this action")
    existing_exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not existing_exam:
        raise HTTPException(status_code=404,
                            detail="Exam does not exist")
    if current_user.id!=existing_exam.faculty_id:
        raise HTTPException(status_code=403,
                            detail="Only faculty who created this exam can perform this action")
    sync_exam_status(existing_exam,db)

    if existing_exam.exam_status!=ExamStatus.draft:
        raise HTTPException(403,"Cannot delete exams which are not draft")
    db.delete(existing_exam)
    db.commit()
    return {"message":"Exam deleted successfully"}

def view_all_exam_service(db:Session,current_user:User):
    if current_user.role!="faculty":
        raise HTTPException("Only faculties can view this")
    exams=db.query(Exam).filter(Exam.faculty_id==current_user.id).all()
    if not exams:
        raise HTTPException(404,"No exam created by this faculty")
    all_exams=[]
    for exam in exams:
        sync_exam_status(exam,db)
        all_exams.append(exam)
    return all_exams


def schedule_exam_service(exam_id:int,scheduled_data:ExamSchedule,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,'Not allowed for this action')
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam: 
        raise HTTPException(404,"Exam not found")
    if exam.faculty_id!=current_user.id:
        raise HTTPException(403,'Not allowed for this action')
    if exam.exam_status!=ExamStatus.draft:
        raise HTTPException(400,'cannot schedule exams which are not draft')
    if not exam.questions or len(exam.questions)==0:
        raise HTTPException(400,"Exam must contain atleast one question before scheduling")
    if not scheduled_data.start_date or not scheduled_data.duration_minutes:
        raise HTTPException(400,'Start date and duration minutes must exist')
    if scheduled_data.start_date<=datetime.now(timezone.utc):
        raise HTTPException(400,"Start date must be in the future")
    if scheduled_data.duration_minutes<=0:
        raise HTTPException(400,'duration minutes must be more than 0')
    
    new_end=scheduled_data.start_date+timedelta(minutes=scheduled_data.duration_minutes)

    existing_exams = db.query(Exam).filter(
    Exam.course_id == exam.course_id,
    Exam.exam_status.in_([ExamStatus.scheduled, ExamStatus.active]),
    Exam.id != exam.id
    ).all()

    for ex in existing_exams:
        existing_end=ex.start_date+timedelta(minutes=ex.duration_minutes)

        # if ex.start_date<new_end and existing_end>scheduled_data.start_date:
        #     overlapping_exam=ex
        #     break

        # if overlapping_exam:
        #     raise HTTPException(400,"An exam already exists in this time window")
    
    calculated_marks = sum(q.max_marks for q in exam.questions)
    
    exam.start_date=scheduled_data.start_date
    exam.duration_minutes=scheduled_data.duration_minutes
    exam.total_marks=calculated_marks
    exam.exam_status=ExamStatus.scheduled

    db.commit()
    db.refresh(exam)

    return exam
    

# Student-Role => Exam Participation

def view_scheduled_exams_service(db:Session,current_user:User):
    if current_user.role!='student':
        raise HTTPException(status_code=403,
                            detail="Only students can view exams")
    exams=db.query(Exam).order_by(Exam.start_date.desc()).all()
    visible_exams=[]
    for exam in exams:
        sync_exam_status(exam,db)
        if exam.exam_status in [ExamStatus.scheduled,ExamStatus.active]:
            visible_exams.append(exam)
    return visible_exams

def register_exam_service(exam_id: int, db: Session, current_user: User):
    if current_user.role != "student":
        raise HTTPException(
            status_code=403,
            detail="Only students can register for the exam"
        )

    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(
            status_code=404,
            detail="Exam not found"
        )

   
    sync_exam_status(exam, db)


    if exam.exam_status != ExamStatus.scheduled:
        raise HTTPException(
            status_code=400,
            detail="Registration is closed for this exam"
        )

   
    existing_attempt = db.query(Attempt).filter(
        Attempt.student_id == current_user.id,
        Attempt.exam_id == exam_id
    ).first()

    if existing_attempt:
        raise HTTPException(
            status_code=403,
            detail="Student can register only once"
        )

    registration = Attempt(
        student_id=current_user.id,
        exam_id=exam_id,
        attempt_status=AttemptStatus.pending
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return {"message": "User registered successfully for the exam"}

def is_attempt_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='student':
        raise  HTTPException(status_code=403,
                            detail="Not allowed for this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(status_code=404,
                            detail="Exam does not exist")
    attempt=db.query(Attempt).filter(and_(Attempt.student_id==current_user.id,
                                                Attempt.exam_id==exam_id)).first()
    if not attempt:
        raise HTTPException(status_code=403,
                            detail="Student must be registered to attempt the exam")
    if attempt.attempt_status!=AttemptStatus.pending:
        raise HTTPException(status_code=403,
                            detail="Student already attempted exam")
    sync_exam_status(exam,db)

    if exam.exam_status!=ExamStatus.active:
        raise HTTPException(status_code=403,
                            detail="Only active exams can be attempted")
    db.commit()
    db.refresh(attempt)

    return attempt

# ADDITION OF QUESTION AND ANSWER ROUTE
def view_exam_questions_objective_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='student':
        raise HTTPException(403,"Only student can perform this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.active:
        raise HTTPException(400,"Cannot show questions for exam that are not active")
    attempt=db.query(Attempt).filter(and_(Attempt.student_id==current_user.id,
                                                Attempt.exam_id==exam_id)).first()
    if not attempt:
        raise HTTPException(status_code=403,
                            detail="Student must be registered to attempt the exam")
    return exam.questions


def answer_exam_questions_service(exam_id:int,question_id:int,response_data:StudentResponse,db:Session,current_user:User):
    if current_user.role!='student':
        raise HTTPException(403,'Only students can answer questions')
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,'Exam not found')
    if exam.exam_status!=ExamStatus.active:
        raise HTTPException(400,"Only active exams can be attempted")
    attempt=db.query(Attempt).filter(Attempt.student_id==current_user.id,Attempt.exam_id==exam_id).first()
    if not attempt:
        raise HTTPException(400,"Only registered students can attempt the exam")
    if attempt.attempt_status!=AttemptStatus.pending:
        raise HTTPException(400,"This question can't be attempted anymore")
    exam_question=db.query(exam_question_association).filter(exam_question_association.c.exam_id==exam_id,
                                                exam_question_association.c.question_id==question_id).first()
    if not exam_question:
        raise HTTPException(400,"Question does not belong to this exam")
    existing_answer = db.query(StudentAnswer).filter(
    StudentAnswer.exam_id == exam_id,
    StudentAnswer.student_id == current_user.id,
    StudentAnswer.question_id == question_id
    ).first()

    if exam.exam_type == "objective":
        if not response_data.selected_option:
            raise HTTPException(400, "Objective exam requires selected option")
        response_data.answer_text = None

    elif exam.exam_type == "subjective":
        if not response_data.answer_text:
            raise HTTPException(400, "Subjective exam requires answer text")
        response_data.selected_option = None

    if existing_answer:
        existing_answer.selected_option = response_data.selected_option
        existing_answer.answer_text = response_data.answer_text
        existing_answer.saved_at = datetime.now(timezone.utc)

    else:
        new_answer = StudentAnswer(
            exam_id=exam_id,
            student_id=current_user.id,
            question_id=question_id,
            selected_option=response_data.selected_option,
            answer_text=response_data.answer_text,
            saved_at=datetime.now(timezone.utc)
        )
        db.add(new_answer)

    db.commit()
    return {
    "question_id": question_id,
    "status": "saved"
    }



def submit_exam_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='student':
        raise HTTPException(status_code=403,
                            detail="Only student can submit exams")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(status_code=404,
                            detail="Exam not found")
    attempt=db.query(Attempt).filter(and_(Attempt.student_id==current_user.id,Attempt.exam_id==exam_id)).first()
    sync_exam_status(exam,db)
    if exam.exam_status==ExamStatus.closed:
        attempt.attempt_status=AttemptStatus.expired
        attempt.auto_submitted=True
    else:
        attempt.attempt_status=AttemptStatus.submitted
        attempt.auto_submitted=False
    db.commit()
    db.refresh(attempt)

    return {"message":"Exam finalized successfully",
            "final_status":attempt.attempt_status,
            "auto_submitted":attempt.auto_submitted,
            "submitted_at":attempt.submitted_at}


# Faculty => Evaluating answers

def view_attempts_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty can view this")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.closed:
        raise HTTPException(400,"Cannot show attempts for exams other than closed")
    attempts=db.query(Attempt).filter(Attempt.exam_id==exam_id).all()
    return attempts

def view_answers_service(exam_id:int,student_id:int,question_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,"Only faculty can access this")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    if exam.faculty_id!=current_user.id:
        raise HTTPException(403,"You cannot view answers for this exam")
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.closed:
        raise HTTPException(400,"Cannot show answers for this exam")
    answer=db.query(StudentAnswer).filter(StudentAnswer.exam_id==exam_id,
                                          StudentAnswer.student_id==student_id,
                                          StudentAnswer.question_id==question_id).first()
    if not answer:
        raise HTTPException(400,"Something is wrong")
    return answer
    

def exam_evaluation_service(new_evaluation:EvaluationIn,exam_id:int,student_id:int,attempt_id:int,db:Session,current_user:User):
    if current_user.role!="faculty":
        raise HTTPException(403,"Not allowed for this action")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(400,"Exam does not exist")
    sync_exam_status(exam,db)
    if exam.exam_status!=ExamStatus.closed:
        raise HTTPException(400,"Cannot start evaluation for exams which are not closed")
    attempt = db.query(Attempt).filter(Attempt.id==attempt_id,Attempt.exam_id==exam_id,Attempt.student_id==student_id).first()
    if not attempt:
        raise HTTPException(400,"No attempt found")
    if attempt.attempt_status not in[AttemptStatus.submitted,AttemptStatus.expired]:
        raise HTTPException(400,"Cannot evaluate for this right now")
    
    if new_evaluation.marks_scored>exam.total_marks:
        raise HTTPException(400,"Marks cannot be greater than total marks")
    if new_evaluation.marks_scored<0:
        raise HTTPException(400,"Marks cannot be less than 0")
    
    existing_evaluation=db.query(Evaluation).filter(Evaluation.attempt_id==attempt_id).first()
    if existing_evaluation:
        raise HTTPException(400,"Evaluation already exists")
    evaluation=Evaluation(exam_id=exam_id,
                          student_id=student_id,
                          attempt_id=attempt_id,
                          marks_scored=new_evaluation.marks_scored,
                          remarks=new_evaluation.remarks)
    db.add(evaluation)
    attempt.attempt_status=AttemptStatus.evaluated
    db.commit()
    db.refresh(evaluation)

    return evaluation

def result_publication_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='faculty':
        raise HTTPException(403,'Not allowed for this action')
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    attempt=db.query(Attempt).filter(Attempt.exam_id==exam_id,Attempt.attempt_status==AttemptStatus.evaluated).first()
    if not attempt:
        raise HTTPException(400,"Evaluated attempt not found")
    exam.exam_status=ExamStatus.evaluated
    db.commit()
    db.refresh(exam)

    print("Status:",exam.exam_status)
    
    return {"message":"Result for the exam published"}

# Student => View results

def view_published_result_service(exam_id:int,db:Session,current_user:User):
    if current_user.role!='student':
        raise HTTPException(403,"Only student can view results")
    exam=db.query(Exam).filter(Exam.id==exam_id).first()
    if not exam:
        raise HTTPException(404,"Exam not found")
    if exam.exam_status!=ExamStatus.evaluated:
        raise HTTPException(403,"Result not published yet for this exam")
    attempt=db.query(Attempt).filter(Attempt.exam_id==exam_id,Attempt.student_id==current_user.id,Attempt.attempt_status==AttemptStatus.evaluated).first()
    if not attempt:
        raise HTTPException(404,"No attempt found")
    evaluation=db.query(Evaluation).filter(Evaluation.exam_id==exam_id,Evaluation.student_id==current_user.id).first()
    if not evaluation:
        raise HTTPException(403,"Result not published yet")
    marks_scored=evaluation.marks_scored
    total=exam.total_marks
    percentage=(marks_scored/total)*100
    result={'exam_id':exam_id,
            'exam_title':exam.title,
            'student_id':current_user.id,
            'total_marks':exam.total_marks,
            'obtained_marks':evaluation.marks_scored,
            'percentage':percentage,
            'attempt_status':attempt.attempt_status}
    return result
  