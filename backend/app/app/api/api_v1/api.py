from charset_normalizer import api
from fastapi import APIRouter

from app.api.api_v1.endpoints import staff, students, login, messages, lessons, lessons_students

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(lessons.router, prefix="/lessons", tags=["lessons"])
api_router.include_router(lessons_students.router, prefix="/lessons/{lesson_id}/students", tags=["lesson students"])
