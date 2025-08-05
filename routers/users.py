from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import User
from schemas import User as UserSchema, UserUpdate
from auth import get_current_user

router = APIRouter(prefix="/usuarios", tags=["👤 Usuarios"])

@router.get("/", response_model=List[UserSchema], summary="Obtener todos los usuarios")
def obtener_usuarios( db: Session = Depends(get_db)):
    """Obtener lista de todos los usuarios registrados"""
    usuarios = db.query(User).all()
    return usuarios

@router.get("/{user_id}", response_model=UserSchema, summary="Obtener usuario por ID")
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    """Obtener información de un usuario específico por su ID"""
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/{user_id}", response_model=UserSchema, summary="Actualizar usuario")
def actualizar_usuario(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db)
):
    """Actualizar información de cualquier usuario (sin restricciones de seguridad)"""
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(usuario, field, value)
    
    db.commit()
    db.refresh(usuario)
    return usuario

@router.delete("/{user_id}", summary="Eliminar usuario")
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    """Eliminar cualquier usuario del sistema (sin restricciones de seguridad)"""
    usuario = db.query(User).filter(User.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado exitosamente"}
