from http.client import HTTPException
from unittest.mock import Mock
from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.controllers.task_controller import task_router, get_task_repo
from app.models.task_model import Task
from app.services.task_service import TaskService

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(task_router)
    return TestClient(app)

@pytest.fixture()
def mock_task_service():
    mock = Mock(spec=TaskService)
    return mock

@pytest.fixture
def mock_task_repo(mock_task_service):
    mock_repo = Mock()
    mock_repo.return_value = mock_task_service
    return mock_repo

@pytest.fixture
def test_create_task_endpoint(client, mock_task_service):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    task = Task(id=1, title="Fazer PI", description="Desenvolver o Projeto Integrador", status="Concluído", created_at=datetime.today())
    mock_task_service.create_task.return_value = task

    response = client.post("/tasks",
                           json={"title": "Fazer PI", "description": "Desenvolver o Projeto Integrador",
                                 "status": "Concluído", "created_at": datetime.today()})

    assert response.status_code == 201
    assert response.json()['title'] == "Fazer PI"

def test_find_task_by_id_not_found(client, mock_task_service):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    mock_task_service.read_user.return_value = None

    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_delete_task_success(client, mock_task_service):
    client.app.dependency_overrides[get_task_repo] = lambda: mock_task_service
    task_id = 1
    task = Task(id=1, title="Fazer PI", description="Desenvolver o Projeto Integrador", status="Concluído", created_at=datetime.today())
    mock_task_service.read.return_value = task
    mock_task_service.delete.return_value = task_id

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    mock_task_repo.read.assert_called_with(task_id)
    mock_task_service.delete.assert_called_once_with(task)


def test_update_task_success(client, mock_task_service):
    client.app.dependency_overrides[get_task_repo] = lambda: mock_task_service
    task_updated = Task(title="Terminar PI")
    updated_task = Task(id=1, title="Fazer PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today())
    mock_task_service.update_task.return_value = updated_task

    response = client.delete("/tasks/1", json=task_updated)
    assert response.status_code == 201
    assert response.json()['title'] == "Terminar PI"


def test_update_user_not_found(client, mock_task_service):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    task_update = Task(email="newjohn@example.com")
    mock_task_service.update_user.side_effect = HTTPException(BaseException)

    response = client.put("/tasks/999", json=task_update.model_dump(exclude_unset=True))

    assert response.status_code == 404
    assert "User not found" in response.json()['detail']


def test_find_all_users(client, mock_user_repo, mock_task_service):
    client.app.dependency_overrides[TaskService] = lambda: mock_task_service
    client.app.dependency_overrides[get_task_repo] = lambda: mock_task_repo

    mock_tasks = [
        Task(id=1, title="Terminar PI", description="Desenvolver o Projeto Integrador", status="Concluído",
                created_at=datetime.today()),
        Task(id=1, title="Terminar Proj.Prog", description="Terminar Projeto de Prog.multiplataforma", status="Em Progresso",
             created_at=datetime.today())
    ]
    mock_user_repo.find_all.return_value = mock_tasks

    response = client.get("/tasks")

    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data) == 2
    assert response_data[0]['title'] == "Terminar PI"
    assert response_data[1]['title'] == "Terminar Proj.Prog"
