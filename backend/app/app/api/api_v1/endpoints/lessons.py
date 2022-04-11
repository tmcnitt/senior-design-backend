from typing import Any, List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.Lesson])
def lessons(
    *,
    db: Session = Depends(deps.get_db),
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user),
) -> Any:
    """
    Get lessons for student or staff
    """
    if isinstance(current_user, models.Student):
        return crud.lesson.get_by_student(db, student_id=current_user.id)
    else:
        return crud.lesson.get_by_staff(db, staff_id=current_user.id)


@router.get("/{lesson_id}", response_model=schemas.Lesson)
def lessons(
    *,
    db: Session = Depends(deps.get_db),
    lesson_id: int,
    current_user: Union[models.Staff,models.Student] = Depends(deps.get_current_user),
) -> Any:
    """
    Get lessons for student or staff
    """
    lesson = crud.lesson.get(db, id=lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=400,
            detail="That lesson does not exist.",
        )

   
    if isinstance(current_user, models.Student):
        lesson_student = crud.lesson_student.get_by_lesson_student(db, lesson_id=lesson_id, student_id=current_user.id)
        if lesson_student is None:
            raise HTTPException(
                status_code=401,
                detail="You do not have access to that lesson.",
            )
        
    else:
        if lesson.staff_id != current_user.id:
            raise HTTPException(
                status_code=401,
                detail="You do not own that lesson.",
            )
        
    return lesson
   
@router.post("/", response_model=schemas.Lesson)
def create(*,  
    db: Session = Depends(deps.get_db), 
    current_user: models.Staff = Depends(deps.get_current_staff_user), 
    lesson_in: schemas.LessonCreate
) -> Any:
    """
    Create a new lesson
    """

    return crud.lesson.create(db, obj_in=lesson_in, staff_id=current_user.id)


@router.put("/{lesson_id}", response_model=schemas.Lesson)
def update(*,  
    db: Session = Depends(deps.get_db), 
    current_user: models.Staff = Depends(deps.get_current_staff_user), 
    lesson_id: int,
    lesson_in: schemas.LessonUpdate
) -> Any:
    """
    Update a lesson
    """
    db_obj = crud.lesson.get(db, lesson_id)

    if db_obj is None:
        raise HTTPException(
            status_code=400,
            detail="That lesson does not exist.",
        )

    if db_obj.staff_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="You do not own that lesson.",
        )
    
    if lesson_in.title is not None:
        db_obj.title = lesson_in.title

    if lesson_in.content is not None:
        db_obj.content = lesson_in.content

    db.commit()
    db.refresh(db_obj)
    return db_obj

@router.delete("/{lesson_id}")
def delete(*,  
    db: Session = Depends(deps.get_db), 
    lesson_id: int,
    current_user: models.Staff = Depends(deps.get_current_staff_user), 
) -> Any:
    """
    Delete a lesson
    """
    lesson = crud.lesson.get(db, lesson_id)

    if lesson is None:
        raise HTTPException(
            status_code=400,
            detail="That lesson does not exist.",
        )

    if lesson.staff_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="You do not own that lesson.",
        )
    
    crud.lesson_student.delete_lesson(db, lesson_id=lesson.id)
    crud.lesson.remove(db, id=lesson.id)