from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Module, Course
from schemas import Module as ModuleSchema, ModuleCreate, ModuleUpdate

router = APIRouter(prefix="/modulos", tags=["🧩 Módulos"])

@router.get("/cursos/{course_id}/modulos/", response_model=List[ModuleSchema], summary="Obtener módulos de un curso")
def obtener_modulos_curso(course_id: str, db: Session = Depends(get_db)):
    """Obtener todos los módulos de un curso específico"""
    # Verificar que el curso existe
    curso = db.query(Course).filter(Course.id == course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    modulos = db.query(Module).filter(Module.course_id == course_id).order_by(Module.position).all()
    return modulos

@router.get("/{module_id}", response_model=ModuleSchema, summary="Obtener módulo por ID")
def obtener_modulo(module_id: str, db: Session = Depends(get_db)):
    """Obtener información de un módulo específico por su ID"""
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    return modulo

@router.post("/", response_model=ModuleSchema, summary="Crear nuevo módulo")
def crear_modulo(modulo: ModuleCreate, db: Session = Depends(get_db)):
    """Crear un nuevo módulo (sin autenticación requerida)"""
    # Verificar que el curso existe
    curso = db.query(Course).filter(Course.id == modulo.course_id).first()
    if curso is None:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    # Verificar si el módulo ya existe
    db_modulo = db.query(Module).filter(Module.id == modulo.id).first()
    if db_modulo:
        raise HTTPException(status_code=400, detail="El ID del módulo ya existe")
    
    db_modulo = Module(**modulo.dict())
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

@router.put("/{module_id}", response_model=ModuleSchema, summary="Actualizar módulo")
def actualizar_modulo(
    module_id: str, 
    module_update: ModuleUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar información de cualquier módulo (sin autenticación requerida)"""
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    update_data = module_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(modulo, field, value)
    
    db.commit()
    db.refresh(modulo)
    return modulo

@router.delete("/{module_id}", summary="Eliminar módulo")
def eliminar_modulo(module_id: str, db: Session = Depends(get_db)):
    """Eliminar cualquier módulo del sistema (sin autenticación requerida)"""
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    db.delete(modulo)
    db.commit()
    return {"mensaje": "Módulo eliminado exitosamente"}
