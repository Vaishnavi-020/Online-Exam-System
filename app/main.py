from fastapi import FastAPI
from app.database import engine
from app.models.base import Base
import app.models
from app.route.auth_router import router as auth_router
from app.route.course_router import router as course_router
from app.route.exam_router import router as exam_router
from app.route.question_router import router as question_router

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(course_router)
app.include_router(exam_router)
app.include_router(question_router)
