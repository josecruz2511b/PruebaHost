from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import ExerciseAttempt, Lesson, User
from schemas import ExerciseAttempt as ExerciseAttemptSchema, ExerciseSubmission
from auth import get_current_user

router = APIRouter(prefix="/ejercicios", tags=["🧪 Ejercicios / Intentos"])

@router.post("/{lesson_id}/enviar", response_model=ExerciseAttemptSchema, summary="Enviar ejercicio")
def enviar_ejercicio(
    lesson_id: int,
    submission: ExerciseSubmission,
    user_id: int,  # Ahora se pasa como parámetro en lugar de obtenerlo del token
    db: Session = Depends(get_db)
):
    """Enviar un ejercicio para evaluación (sin autenticación requerida)"""
    # Verificar que la lección existe
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if leccion is None:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    # Verificar que el usuario existe
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Validación simple - verificar si el código enviado coincide con la solución
    is_correct = submission.code_submitted.strip() == leccion.practice_solution.strip()
    
    # Crear intento de ejercicio
    intento = ExerciseAttempt(
        user_id=user_id,
        lesson_id=lesson_id,
        code_submitted=submission.code_submitted,
        is_correct=is_correct
    )
    
    db.add(intento)
    db.commit()
    db.refresh(intento)
    return intento

@router.get("/intentos", response_model=List[ExerciseAttemptSchema], summary="Obtener todos los intentos")
def obtener_todos_intentos(
    skip: int = 0,
    limit: int = 100,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener todos los intentos de ejercicios (opcionalmente filtrar por usuario)"""
    query = db.query(ExerciseAttempt)
    
    if user_id:
        query = query.filter(ExerciseAttempt.user_id == user_id)
    
    intentos = query.offset(skip).limit(limit).all()
    return intentos

@router.get("/{lesson_id}/ultimo-intento", response_model=ExerciseAttemptSchema, summary="Obtener último intento")
def obtener_ultimo_intento(
    lesson_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Obtener el último intento de un usuario para una lección específica"""
    # Verificar que la lección existe
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if leccion is None:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    intento = db.query(ExerciseAttempt).filter(
        ExerciseAttempt.user_id == user_id,
        ExerciseAttempt.lesson_id == lesson_id
    ).order_by(ExerciseAttempt.attempt_date.desc()).first()
    
    if intento is None:
        raise HTTPException(status_code=404, detail="No se encontraron intentos para esta lección")
    
    return intento

@router.delete("/intentos/{attempt_id}", summary="Eliminar intento")
def eliminar_intento(attempt_id: int, db: Session = Depends(get_db)):
    """Eliminar un intento de ejercicio específico"""
    intento = db.query(ExerciseAttempt).filter(ExerciseAttempt.id == attempt_id).first()
    if intento is None:
        raise HTTPException(status_code=404, detail="Intento no encontrado")
    
    db.delete(intento)
    db.commit()
    return {"mensaje": "Intento eliminado exitosamente"}
