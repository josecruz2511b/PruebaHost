from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Esquemas de Usuario
class UsuarioBase(BaseModel):
    nombre: str = None
    email: EmailStr

class UsuarioCrear(UsuarioBase):
    nombre: str
    password: str

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    imagen: Optional[str] = None

class Usuario(BaseModel):
    id: int
    name: str
    email: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Autenticación
class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Esquemas de Curso
class CursoBase(BaseModel):
    titulo: str
    descripcion: str
    icono: str
    clase_color: str

class CursoCrear(CursoBase):
    id: str

class CursoActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    icono: Optional[str] = None
    clase_color: Optional[str] = None

class Curso(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    color_class: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Módulo
class ModuloBase(BaseModel):
    titulo: str
    descripcion: str
    posicion: int

class ModuloCrear(ModuloBase):
    id: str
    curso_id: str

class ModuloActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    posicion: Optional[int] = None

class Modulo(BaseModel):
    id: str
    course_id: str
    title: str
    description: str
    position: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Lección
class LeccionBase(BaseModel):
    titulo: str
    teoria: str
    instrucciones_practica: str
    codigo_inicial_practica: str
    solucion_practica: str
    posicion: int

class LeccionCrear(LeccionBase):
    modulo_id: str

class LeccionActualizar(BaseModel):
    titulo: Optional[str] = None
    teoria: Optional[str] = None
    instrucciones_practica: Optional[str] = None
    codigo_inicial_practica: Optional[str] = None
    solucion_practica: Optional[str] = None
    posicion: Optional[int] = None

class Leccion(BaseModel):
    id: int
    module_id: str
    title: str
    theory: str
    practice_instructions: str
    practice_initial_code: str
    practice_solution: str
    position: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Progreso
class ProgresoUsuarioBase(BaseModel):
    usuario_id: int
    modulo_id: str
    completado: bool = False

class ProgresoUsuarioCrear(ProgresoUsuarioBase):
    pass

class ProgresoUsuarioActualizar(BaseModel):
    completado: Optional[bool] = None
    fecha_completado: Optional[datetime] = None

class ProgresoUsuario(BaseModel):
    id: int
    user_id: int
    module_id: str
    completed: bool
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas de Intento de Ejercicio
class IntentoEjercicioBase(BaseModel):
    codigo_enviado: str
    es_correcto: bool

class IntentoEjercicioCrear(IntentoEjercicioBase):
    usuario_id: int
    leccion_id: int

class IntentoEjercicio(BaseModel):
    id: int
    user_id: int
    lesson_id: int
    code_submitted: str
    is_correct: bool
    attempt_date: datetime
    
    class Config:
        from_attributes = True

class EnvioEjercicio(BaseModel):
    codigo_enviado: str
