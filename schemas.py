from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    image: Optional[str] = None

class User(UserBase):
    id: int
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Course schemas
class CourseBase(BaseModel):
    title: str
    description: str
    icon: str
    color_class: str

class CourseCreate(CourseBase):
    id: str

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color_class: Optional[str] = None

class Course(CourseBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Module schemas
class ModuleBase(BaseModel):
    title: str
    description: str
    position: int

class ModuleCreate(ModuleBase):
    id: str
    course_id: str

class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    position: Optional[int] = None

class Module(ModuleBase):
    id: str
    course_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Lesson schemas
class LessonBase(BaseModel):
    title: str
    theory: str
    practice_instructions: str
    practice_initial_code: str
    practice_solution: str
    position: int

class LessonCreate(LessonBase):
    module_id: str

class LessonUpdate(BaseModel):
    title: Optional[str] = None
    theory: Optional[str] = None
    practice_instructions: Optional[str] = None
    practice_initial_code: Optional[str] = None
    practice_solution: Optional[str] = None
    position: Optional[int] = None

class Lesson(LessonBase):
    id: int
    module_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Progress schemas
class UserProgressBase(BaseModel):
    user_id: int
    module_id: str
    completed: bool = False

class UserProgressCreate(UserProgressBase):
    pass

class UserProgressUpdate(BaseModel):
    completed: Optional[bool] = None
    completion_date: Optional[datetime] = None

class UserProgress(UserProgressBase):
    id: int
    completion_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Exercise Attempt schemas
class ExerciseAttemptBase(BaseModel):
    code_submitted: str
    is_correct: bool

class ExerciseAttemptCreate(ExerciseAttemptBase):
    user_id: int
    lesson_id: int

class ExerciseAttempt(ExerciseAttemptBase):
    id: int
    user_id: int
    lesson_id: int
    attempt_date: datetime
    
    class Config:
        from_attributes = True

class ExerciseSubmission(BaseModel):
    code_submitted: str
