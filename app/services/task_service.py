import logging

from fastapi import HTTPException
from pydantic import TypeAdapter
from sqlalchemy.exc import IntegrityError

from app.models.task_model import Task
from app.repositories.task_repository import ITaskRepository

logger = logging.getLogger("fastapi")


class ITaskService:

    def create_task(self, task_data: object):
        raise NotImplementedError

    def read_task(self, task_id: int):
        raise NotImplementedError

    def update_task(self, task_id: int, task_update: object):
        raise NotImplementedError

    def delete_task(self, task_id: int):
        raise NotImplementedError


class TaskService(ITaskService):
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    def create_task(self, task_data: Task) -> Task:
        task = Task(**task_data.model_dump())
        try:
            logger.info("Creating task: %s", task)
            created_task = self.task_repository.create(task)
        except IntegrityError as e:
            logger.error("Error creating task: %s. Detail: %s", task, e)
            raise HTTPException(status_code=409, detail=f"Task already exists. Error: {e.args[0]}")
        return TypeAdapter(Task).validate_python(created_task)

    def read_task(self, task_id: int) -> Task:
        logger.info("Reading task with id id %s", task_id)
        task = self.task_repository.read(task_id)
        if task is None:
            logger.error("Task with id %s not found", task_id)
            raise HTTPException(status_code=404, detail="User not found")
        return TypeAdapter(Task).validate_python(task)

    def find_all(self) -> list[Task]:
        logger.info("Finding all tasks")
        tasks = self.task_repository.find_all()
        return [TypeAdapter(Task).validate_python(task) for task in tasks]

    def update_task(self, task_id: int, task_data: Task) -> Task:
        logger.info("Updating task with id %s", task_id)
        task = self.task_repository.read(task_id)
        if task is None:
            logger.error("Task with id %s not found", task_id)
            raise HTTPException(status_code=404, detail="Task not found")
        task_data = task_data.model_dump(exclude_unset=True)
        for key, value in task_data.items():
            setattr(task, key, value)
        updated_task = self.task_repository.update(task, task_data)
        return TypeAdapter(Task).validate_python(updated_task)

    def delete_task(self, task_id: int) -> int:
        logger.info("Deleting task with id %s", task_id)
        task = self.task_repository.read(task_id)
        if task is None:
            logger.info("Task with id %s not found", task_id)
            raise HTTPException(status_code=404, detail="Task not found")
        delete_id = self.task_repository.delete(task)
        return delete_id
