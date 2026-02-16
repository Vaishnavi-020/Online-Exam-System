# Online Examination System

## 📌 Project Overview
A full-stack web application for conducting and managing online examinations. The system supports Faculty and Student roles with secure authentication, exam creation, and automated state changes for exam states.

---

## 🚀 Features

### Faculty
- Create Courses
- Create Exams
- Update exams
- Add questions
- Delete questions
- View student attempts
- Evaluate results

### Student
- Register and Login
- Attempt exams
- Save and submit answers
- View active exams
- View results

### System
- Role-based Authentication
- JWT authorization
- Auto evaluation of total marks for a given exam

---

## Tech Stack

Backend:
- Python
- FastAPI
- SQLAlchemy
- JWT

Frontend:
- React
- Tailwind CSS

Database:
- Postgresql

---

## 📂 Project Structure

Backend:
app/
Enum/
models/
route/
schemas/
service/

Frontend:
src/
components/
pages/

---

## Installation Guide:

Backend:
- pip install -r requirements.txt
- uvicorn app.main:app --reload

Frontend:
- npm install
- npm run dev

## Future Improvements
- History of exams attempted
- Rank of student in a particular exam
- Deployment
- Dockerization 
