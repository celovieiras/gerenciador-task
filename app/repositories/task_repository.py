from sqlalchemy.orm import Session

from app.models.task_model import Task


class ITaskRepository:
    def create(self, task: object):
        raise NotImplementedError

    def read(self, task_id: int):
        raise NotImplementedError

    def update(self, task: object, task_data: dict):
        raise NotImplementedError

    def delete(self, task: object):
        raise NotImplementedError


class TaskRepository(ITaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, task: object) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh()
        return task

    def update(self, task: Task, task_data) -> Task:
        for key, value in task_data.items():
            setattr(task, key, value)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task) -> int:
        task_id = task.id
        self.session.delete(task)
        self.session.commit()
        return task_id

    def read(self, task_id):
        return self.session.query(Task).filter(Task.id == task_id).first()

    def find_all(self):
        return self.session.query(Task).all()