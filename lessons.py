from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Lesson, Module
from schemas import Lesson as LessonSchema, LessonCreate, LessonUpdate

router = APIRouter(prefix="/lecciones", tags=["📖 Lecciones"])

@router.get("/modulos/{module_id}/lecciones/", response_model=List[LessonSchema], summary="Obtener lecciones de un módulo")
def obtener_lecciones_modulo(module_id: str, db: Session = Depends(get_db)):
    """Obtener todas las lecciones de un módulo específico"""
    # Verificar que el módulo existe
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    lecciones = db.query(Lesson).filter(Lesson.module_id == module_id).order_by(Lesson.position).all()
    return lecciones

@router.get("/{lesson_id}", response_model=LessonSchema, summary="Obtener lección por ID")
def obtener_leccion(lesson_id: int, db: Session = Depends(get_db)):
    """Obtener información de una lección específica por su ID"""
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if leccion is None:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    return leccion

@router.post("/", response_model=LessonSchema, summary="Crear nueva lección")
def crear_leccion(leccion: LessonCreate, db: Session = Depends(get_db)):
    """Crear una nueva lección (sin autenticación requerida)"""
    # Verificar que el módulo existe
    modulo = db.query(Module).filter(Module.id == leccion.module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    db_leccion = Lesson(**leccion.dict())
    db.add(db_leccion)
    db.commit()
    db.refresh(db_leccion)
    return db_leccion

@router.put("/{lesson_id}", response_model=LessonSchema, summary="Actualizar lección")
def actualizar_leccion(
    lesson_id: int, 
    lesson_update: LessonUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar información de cualquier lección (sin autenticación requerida)"""
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if leccion is None:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    update_data = lesson_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(leccion, field, value)
    
    db.commit()
    db.refresh(leccion)
    return leccion

@router.delete("/{lesson_id}", summary="Eliminar lección")
def eliminar_leccion(lesson_id: int, db: Session = Depends(get_db)):
    """Eliminar cualquier lección del sistema (sin autenticación requerida)"""
    leccion = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if leccion is None:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    
    db.delete(leccion)
    db.commit()
    return {"mensaje": "Lección eliminada exitosamente"}
