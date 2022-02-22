from charset_normalizer import api
from fastapi import APIRouter

from app.api.api_v1.endpoints import staff, students, login, messages
#from app.api.api_v1.endpoints import login, users, staff

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(staff.router, prefix="/staff", tags=["staff"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])

#api_router.include_router(login.router, tags=["login"])
#api_router.include_router(users.router, prefix="/users", tags=["users"])
