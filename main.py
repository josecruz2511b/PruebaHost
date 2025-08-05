from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, users, courses, modules, lessons, exercises, progress

# Crear tablas de la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CodeMastery API",
    description="""
    ## API completa para la plataforma de aprendizaje CodeMastery
    
    Esta API proporciona endpoints para gestionar:
    
    * **🔐 Autenticación** - Registro, login y gestión de usuarios
    * **👤 Usuarios** - CRUD completo de usuarios
    * **📚 Cursos** - Gestión de cursos de programación
    * **🧩 Módulos** - Organización de contenido por módulos
    * **📖 Lecciones** - Contenido educativo detallado
    * **🧪 Ejercicios** - Sistema de práctica y evaluación
    * **🏁 Progreso** - Seguimiento del avance de los estudiantes
    
    ### Características principales:
    - Operaciones CRUD sin restricciones de seguridad
    - Documentación automática con Swagger UI
    - Conexión directa a base de datos MySQL
    - Mensajes y respuestas completamente en español
    """,
    version="2.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, reemplazar con orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(exercises.router)
app.include_router(progress.router)

@app.get("/", tags=["🏠 Inicio"])
def inicio():
    """Endpoint de bienvenida con información de la API"""
    return {
        "mensaje": "¡Bienvenido a CodeMastery API!",
        "descripcion": "API completa para gestión de cursos de programación",
        "documentacion": "/docs",
        "documentacion_alternativa": "/redoc",
        "version": "2.0.0",
        "caracteristicas": [
            "CRUD completo sin restricciones de seguridad",
            "Interfaz completamente en español",
            "Documentación automática",
            "Conexión directa a MySQL"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
