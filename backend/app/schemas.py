from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

 
# 1. Definisi nilai status yang valid
class TaskStatus(str, Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


# 2. Schema untuk data input saat membuat task baru (POST /tasks)
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Judul tidak boleh kosong")
    description: Optional[str] = Field(None, description="Deskripsi tugas opsional")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Status tugas")


# 3. Schema untuk data input saat update task (PUT /tasks/{id})
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


# 4. Schema format data yang dikirim balik ke frontend (Response)
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    created_at: datetime

    class Config:
        from_attributes = True