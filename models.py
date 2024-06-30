from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: Optional[int] = Field(default=None)
    name: str
    email: str

class Task(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id : int
    title: str
    description: Optional[str]
    completed: bool = False

class Event(BaseModel):
    id: Optional[int]  = Field(default=None)
    user_id : int  = Field(default=None)
    name: str
    date: str

class Note(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id : int = Field(default=None)
    content: str

class UserResponse(BaseModel):
    message : str

class UpdateTaskStatus(BaseModel):
    completed: bool

