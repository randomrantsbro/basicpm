from fastapi import APIRouter, HTTPException
from ..models import Task, UserResponse, UpdateTaskStatus
from ..database import db
from typing import Dict

router = APIRouter()

@router.post("/tasks", response_model=UserResponse)
def create_task(task: Task, user_id: int):
    max_task_id = max((task['id'] for task in db.table('tasks').all() if task['user_id'] == user_id), default=0)
    task.id = max_task_id + 1
    task.user_id = user_id
    db.table('tasks').insert(task.dict())
    tasks_count = sum(1 for task in db.table('tasks').all() if task['user_id'] == user_id)
    return {"message": f"Task Created Successfully. Total tasks for user {user_id}: {tasks_count}"}

@router.get("/view_tasks", response_model=list[Task])
def get_tasks(user_id: int):
    tasks = [task for task in db.table('tasks').all() if task['user_id'] == user_id]
    return tasks
@router.get("/view_all_tasks", response_model=Dict[int, list[Task]])
def get_tasks_by_user_id():
    tasks = db.table('tasks').all()
    tasks_by_user = {}

    for task in tasks:
        user_id = task['user_id']
        if user_id not in tasks_by_user:
            tasks_by_user[user_id] = []
        tasks_by_user[user_id].append(Task(**task))

    return tasks_by_user

@router.get("/view_tasks/{task_id}", response_model=Task)
def get_task(task_id: int, user_id: int):
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"User not found")

    task = db.table('tasks').get(doc_id=task_id)
    if not task or task['user_id'] != user_id:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found for user {user_id}")

    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, user_id: int):
    existing_task = db.table('tasks').get(doc_id=task_id)
    if existing_task['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Task not found for this user")

    db.table('tasks').update(task.dict(), doc_ids=[task_id])
    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int):
    existing_task = db.table('tasks').get(doc_id=task_id)
    if existing_task['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Task not found for this user")

    db.table('tasks').remove(doc_ids=[task_id])
    return {"message": "Task deleted"}

@router.put("/tasks/{task_id}/complete", response_model=Task)
def mark_task_as_complete(task_id: int, update_status: UpdateTaskStatus, user_id: int):
    existing_task = db.table('tasks').get(doc_id=task_id)
    if not existing_task or existing_task['user_id'] != user_id:
        raise HTTPException(status_code=404, detail="Task not found for this user")

    # Update the task's 'completed' status
    db.table('tasks').update({'completed': update_status.completed}, doc_ids=[task_id])

    # Fetch and return the updated task
    updated_task = db.table('tasks').get(doc_id=task_id)
    return updated_task

