from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas

# 1. Inisialisasi tabel database otomatis saat aplikasi start
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Simple Task Project Tracker API")

# 2. Konfigurasi CORS agar frontend (React/Vue) dapat mengakses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Mengizinkan semua origin untuk kebutuhan development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoint 1: Ambil semua daftar tugas
@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).order_by(models.Task.id.desc()).all()
    return tasks


# Endpoint 2: Tambah tugas baru
@app.post("/tasks", response_model=schemas.TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status.value,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# Endpoint 3: Update tugas berdasarkan ID
@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )

    # Hanya update field yang dikirimkan oleh frontend
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field == "status" and value is not None:
            setattr(task, field, value.value if hasattr(value, "value") else value)
        else:
            setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task


# Endpoint 4: Hapus tugas berdasarkan ID
@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tugas dengan ID {task_id} tidak ditemukan",
        )

    db.delete(task)
    db.commit()
    return None