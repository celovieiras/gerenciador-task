from unittest.mock import Mock
from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.models.task_model import Task
from app.services.task_service import TaskService


@pytest.fixture
def mock_user_repo():
    return Mock()


@pytest.fixture
def user_service(mock_task_repo):
    return TaskService(mock_task_repo)


def test_create_task_success(mock_task_repo, task_service):
    task_data = Task(id=1, title="Terminar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())
    mock_task = Task(id=1, **task_data.model_dump())
    mock_task_repo.create.return_value = mock_task

    result = task_service.create_task(task_data)

    assert result.title == "Terminar PI"
    mock_task_repo.create.assert_called_once()


def test_create_task_failure(mock_task_repo, task_service):
    task_data = Task(id=1, title="Terminar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())
    mock_task_repo.create.side_effect = IntegrityError(None, None, BaseException("User already exists"))

    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(task_data)

    assert exc_info.value.status_code == 409
    assert "Task already exists" in str(exc_info.value.detail)


def test_read_task_success(mock_task_repo, task_service):
    task = Task(id=1, title="Terminar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())
    mock_task_repo.read.return_value = task

    result = task_service.read_task(1)

    assert result.id == 1
    assert result.description == "Desenvolver o Projeto Integrador"
    mock_task_repo.read.assert_called_once_with(1)


def test_read_task_not_found(mock_task_repo, task_service):
    mock_task_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.read_task(999)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)


def test_delete_task_success(mock_task_repo, task_service):
    task = Task(id=1,
                title="Terminar PI",
                description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today()
                )

    mock_task_repo.read.return_value = task
    mock_task_repo.delete.return_value = 1

    result = task_service.delete_task(1)

    assert result == 1
    mock_task_repo.delete.assert_called_once_with(user)


def test_delete_task_not_found(mock_task_repo, task_service):
    mock_task_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.delete_task(999)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)


def test_update_task_success(mock_task_repo, task_service):
    original_task = Task(id=1, title="Terminar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())
    task_update_data = Task(title="Finalizar PI")
    updated_task = Task(id=1, title="Finalizar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())

    mock_task_repo.read.return_value = original_task
    mock_task_repo.update.return_value = updated_task

    result = task_service.update_task(1, task_update_data)

    assert result.title == "Finalizar PI"
    mock_task_repo.update.assert_called_once()
    assert mock_task_repo.update.call_args[0][
               0].title == "Finalizar PI"


def test_update_task_not_found(mock_task_repo, task_service):
    task_update_data = Task(titlr="Finalizar PI")
    mock_task_repo.read.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.update_task(999, user_task_data)

    assert exc_info.value.status_code == 404
    assert "User not found" in str(exc_info.value.detail)
    mock_task_repo.read.assert_called_once_with(999)


def test_find_all_tasks(mock_task_repo, task_service):
    tasks = [
        Task(id=1,
             title="Terminar PI",
             description="Desenvolver o Projeto Integrador", status="Concluído",
             created_at=datetime.today()
             ),
        Task(id=2,
             title="Terminar Proj.Prog",
             description="Desenvolver o Projeto Prog.Multiplataforma", status="Concluído",
             created_at=datetime.today()
             )
    ]
    mock_task_repo.find_all.return_value = tasks

    result = task_service.find_all()

    assert len(result) == 2
    assert result[0].name == "John Doe"
    assert result[1].name == "Jane Doe"
    mock_task_repo.find_all.assert_called_once()