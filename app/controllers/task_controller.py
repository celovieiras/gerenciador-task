from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task_model import Task
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_repo(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


@task_router.post("/", status_code=201, description="Search for all tasks", response_model=Task)
def create(request: Task, task_repo: TaskRepository = Depends(get_task_repo)):
    task_service = TaskService(task_repo)
    return task_service.create_task(request)


@task_router.get("/{task_id}", status_code=200, description="Search a task for ID", response_model=Task)
def find_by_id(task_id: int, task_repo: TaskRepository = Depends(get_task_repo)):
    task_service = TaskService(task_repo)
    return task_service.read_task(task_id)


@task_router.put("/{task_id}", status_code=200, description="Update a task", response_model=Task)
def update(task_id: int, request: Task, task_repo: TaskRepository = Depends(get_task_repo)):
    task_service = TaskService(task_repo)
    return task_service.update_task(task_id, request)


@task_router.delete("/{task_id}", status_code=204, description="Delete a task")
def delete(task_id: int, task_repo: TaskRepository = Depends(get_task_repo)):
    task_service = TaskService(task_repo)
    task_service.delete_task(task_id)
