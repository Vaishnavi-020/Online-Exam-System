from datetime import datetime,timezone,timedelta
from app.models.Exam import Exam
from sqlalchemy.orm import Session
from app.Enum.exam_status_enum import ExamStatus

def resolve_exam_status(exam:Exam):
    if exam.start_date is None or exam.duration_minutes is None:
        return exam.exam_status
    now=datetime.now(timezone.utc)

    end_time=exam.start_date+timedelta(minutes=exam.duration_minutes)

    if exam.start_date<=now<=end_time:
        return ExamStatus.active
    elif now>=end_time:
        return ExamStatus.closed
    else:
        return ExamStatus.scheduled
    
def sync_exam_status(exam:Exam,db:Session):
    new_status=resolve_exam_status(exam)

    if exam.exam_status!=new_status:
        exam.exam_status=new_status
        db.commit()
        db.refresh(exam)