from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime, date
from database import get_db
from models import UserProgress, User, Module
from schemas import UserProgress as UserProgressSchema, UserProgressCreate, UserProgressUpdate

router = APIRouter(prefix="/progreso", tags=["🏁 Progreso"])

# 🔍 Consultas (GET)
@router.get("/", response_model=List[UserProgressSchema], summary="Obtener todo el progreso")
def obtener_todo_progreso(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener todo el progreso registrado en el sistema"""
    progreso = db.query(UserProgress).offset(skip).limit(limit).all()
    return progreso

@router.get("/{user_id}", response_model=List[UserProgressSchema], summary="Obtener progreso por usuario")
def obtener_progreso_usuario(user_id: int, db: Session = Depends(get_db)):
    """Obtener progreso por ID de usuario"""
    # Verificar que el usuario existe
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    progreso = db.query(UserProgress).filter(UserProgress.user_id == user_id).all()
    return progreso

@router.get("/curso/{module_id}", response_model=List[UserProgressSchema], summary="Obtener progreso por módulo")
def obtener_progreso_modulo(module_id: str, db: Session = Depends(get_db)):
    """Obtener progreso por módulo"""
    # Verificar que el módulo existe
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    progreso = db.query(UserProgress).filter(UserProgress.module_id == module_id).all()
    return progreso

@router.get("/estado/{estado}", response_model=List[UserProgressSchema], summary="Filtrar por estado")
def obtener_progreso_por_estado(estado: int, db: Session = Depends(get_db)):
    """Filtrar por estado (0: incompleto, 1: completo)"""
    if estado not in [0, 1]:
        raise HTTPException(status_code=400, detail="Estado debe ser 0 (incompleto) o 1 (completo)")
    
    completado = bool(estado)
    progreso = db.query(UserProgress).filter(UserProgress.completed == completado).all()
    return progreso

@router.get("/rango-fechas", response_model=List[UserProgressSchema], summary="Buscar por rango de fechas")
def obtener_progreso_por_fechas(
    start_date: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    end_date: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Buscar por rango de fechas"""
    progreso = db.query(UserProgress).filter(
        and_(
            UserProgress.completion_date >= start_date,
            UserProgress.completion_date <= end_date
        )
    ).all()
    return progreso

@router.get("/usuarios/completos/{module_id}", summary="Usuarios que completaron módulo")
def obtener_usuarios_completos(module_id: str, db: Session = Depends(get_db)):
    """Usuarios que completaron un módulo"""
    # Verificar que el módulo existe
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    usuarios = db.query(User).join(UserProgress).filter(
        and_(
            UserProgress.module_id == module_id,
            UserProgress.completed == True
        )
    ).all()
    
    return [{"user_id": usuario.id, "nombre": usuario.name, "email": usuario.email} for usuario in usuarios]

@router.get("/usuarios/incompletos/{module_id}", summary="Usuarios que no completaron módulo")
def obtener_usuarios_incompletos(module_id: str, db: Session = Depends(get_db)):
    """Usuarios que no completaron un módulo"""
    # Verificar que el módulo existe
    modulo = db.query(Module).filter(Module.id == module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    # Obtener usuarios que han comenzado pero no completado el módulo
    usuarios = db.query(User).join(UserProgress).filter(
        and_(
            UserProgress.module_id == module_id,
            UserProgress.completed == False
        )
    ).all()
    
    return [{"user_id": usuario.id, "nombre": usuario.name, "email": usuario.email} for usuario in usuarios]

@router.get("/resumen/{user_id}", summary="Resumen de progreso del usuario")
def obtener_resumen_usuario(user_id: int, db: Session = Depends(get_db)):
    """Resumen general de progreso del usuario"""
    # Verificar que el usuario existe
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Obtener estadísticas de progreso
    total_modulos = db.query(UserProgress).filter(UserProgress.user_id == user_id).count()
    modulos_completados = db.query(UserProgress).filter(
        and_(UserProgress.user_id == user_id, UserProgress.completed == True)
    ).count()
    
    porcentaje_completado = (modulos_completados / total_modulos * 100) if total_modulos > 0 else 0
    
    return {
        "user_id": user_id,
        "nombre_usuario": usuario.name,
        "total_modulos": total_modulos,
        "modulos_completados": modulos_completados,
        "modulos_incompletos": total_modulos - modulos_completados,
        "porcentaje_completado": round(porcentaje_completado, 2)
    }

# 📝 Inserción (POST)
@router.post("/", response_model=UserProgressSchema, summary="Agregar nuevo progreso")
def crear_progreso(progreso: UserProgressCreate, db: Session = Depends(get_db)):
    """Agregar nuevo registro de progreso (sin autenticación requerida)"""
    # Verificar que el usuario y módulo existen
    usuario = db.query(User).filter(User.id == progreso.user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    modulo = db.query(Module).filter(Module.id == progreso.module_id).first()
    if modulo is None:
        raise HTTPException(status_code=404, detail="Módulo no encontrado")
    
    # Verificar si ya existe progreso para este usuario y módulo
    progreso_existente = db.query(UserProgress).filter(
        and_(
            UserProgress.user_id == progreso.user_id,
            UserProgress.module_id == progreso.module_id
        )
    ).first()
    
    if progreso_existente:
        raise HTTPException(status_code=400, detail="Ya existe progreso para este usuario y módulo")
    
    db_progreso = UserProgress(**progreso.dict())
    if progreso.completed:
        db_progreso.completion_date = datetime.utcnow()
    
    db.add(db_progreso)
    db.commit()
    db.refresh(db_progreso)
    return db_progreso

# 🔄 Actualización (PUT)
@router.put("/", response_model=UserProgressSchema, summary="Actualizar progreso")
def actualizar_progreso(
    user_id: int,
    module_id: str,
    progress_update: UserProgressUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un progreso existente (sin autenticación requerida)"""
    progreso = db.query(UserProgress).filter(
        and_(
            UserProgress.user_id == user_id,
            UserProgress.module_id == module_id
        )
    ).first()
    
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    
    update_data = progress_update.dict(exclude_unset=True)
    
    # Si se marca como completado y no se proporciona fecha de finalización, establecerla ahora
    if update_data.get("completed") and not update_data.get("completion_date"):
        update_data["completion_date"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(progreso, field, value)
    
    db.commit()
    db.refresh(progreso)
    return progreso

# ❌ Eliminación (DELETE)
@router.delete("/{user_id}/{module_id}", summary="Eliminar progreso")
def eliminar_progreso(user_id: int, module_id: str, db: Session = Depends(get_db)):
    """Eliminar progreso de un módulo específico (sin autenticación requerida)"""
    progreso = db.query(UserProgress).filter(
        and_(
            UserProgress.user_id == user_id,
            UserProgress.module_id == module_id
        )
    ).first()
    
    if progreso is None:
        raise HTTPException(status_code=404, detail="Progreso no encontrado")
    
    db.delete(progreso)
    db.commit()
    return {"mensaje": "Progreso eliminado exitosamente"}
