from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Course
from schemas import Course as CourseSchema, CourseCreate, CourseUpdate

router = APIRouter(prefix="/cursos", tags=["📚 Cursos"])

@router.get("/", response_model=List[CourseSchema], summary="Obtener todos los cursos")
def obtener_cursos( db: Session = Depends(get_db)):
    """Obtener lista de todos los cursos disponibles"""
    cursos = db.query(Course).all()
    return cursos

@router.get("/{course_id}", response_model=CourseSchema, summary="Obtener curso por ID")
def obtener_curso(course_id: str, db: Session = Depends(get_db)):
    """Obtener información de un curso específico por su ID"""
    curso = db.query(Course).filter(Course.id == course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso

@router.post("/", response_model=CourseSchema, summary="Crear nuevo curso")
def crear_curso(curso: CourseCreate, db: Session = Depends(get_db)):
    """Crear un nuevo curso (sin autenticación requerida)"""
    # Verificar si el curso ya existe
    db_curso = db.query(Course).filter(Course.id == curso.id).first()
    if db_curso:
        raise HTTPException(status_code=400, detail="El ID del curso ya existe")
    
    db_curso = Course(**curso.dict())
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@router.put("/{course_id}", response_model=CourseSchema, summary="Actualizar curso")
def actualizar_curso(
    course_id: str, 
    course_update: CourseUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar información de cualquier curso (sin autenticación requerida)"""
    curso = db.query(Course).filter(Course.id == course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    update_data = course_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(curso, field, value)
    
    db.commit()
    db.refresh(curso)
    return curso

@router.delete("/{course_id}", summary="Eliminar curso")
def eliminar_curso(course_id: str, db: Session = Depends(get_db)):
    """Eliminar cualquier curso del sistema (sin autenticación requerida)"""
    curso = db.query(Course).filter(Course.id == course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    db.delete(curso)
    db.commit()
    return {"mensaje": "Curso eliminado exitosamente"}
