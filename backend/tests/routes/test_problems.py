import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from tests.utils.problem import create_random_problem


def test_create_problem(client: TestClient) -> None:
    data: dict = {
        "title": "Sample Problem",
        "platform": "leetcode",
        "url": "https://leetcode.com/problems/sample-problem",
        "problem_id": "123",
        "difficulty": "medium",
        "normalized_difficulty": 2,
        "simplified_statement": "This is a sample problem statement.",
        "notes": "These are some sample notes.",
        "solution_url": "https:github.com/user/sample-solution",
    }
    response = client.post(
        f"{settings.API_V1_STR}/problems/",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["platform"] == data["platform"]
    assert content["url"] == data["url"]
    assert content["problem_id"] == data["problem_id"]
    assert content["difficulty"] == data["difficulty"]
    assert content["normalized_difficulty"] == data["normalized_difficulty"]
    assert content["simplified_statement"] == data["simplified_statement"]
    assert content["notes"] == data["notes"]
    assert content["solution_url"] == data["solution_url"]
    assert "id" in content


def test_read_problem(client: TestClient, db: Session) -> None:
    problem = create_random_problem(db)
    response = client.get(
        f"{settings.API_V1_STR}/problems/{problem.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == problem.title
    assert content["platform"] == problem.platform
    assert content["url"] == problem.url
    assert content["problem_id"] == problem.problem_id
    assert content["difficulty"] == problem.difficulty
    assert content["normalized_difficulty"] == problem.normalized_difficulty
    assert content["simplified_statement"] == problem.simplified_statement
    assert content["notes"] == problem.notes
    assert content["solution_url"] == problem.solution_url
    assert content["id"] == str(problem.id)


def test_read_problem_not_found(client: TestClient) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/problems/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Problem not found"


def test_read_problems(client: TestClient, db: Session) -> None:
    create_random_problem(db)
    create_random_problem(db)
    response = client.get(
        f"{settings.API_V1_STR}/problems/",
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_problem(client: TestClient, db: Session) -> None:
    problem = create_random_problem(db)
    data: dict = {
        "title": "Updated title",
        "platform": "leetcode",
        "url": "https://leetcode.com/problems/updated-problem",
        "problem_id": "456",
        "difficulty": "hard",
        "normalized_difficulty": 8,
        "simplified_statement": "This is an updated problem statement.",
        "notes": "These are some updated notes.",
        "solution_url": "https://github.com/user/updated-solution",
    }
    response = client.put(
        f"{settings.API_V1_STR}/problems/{problem.id}",
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["platform"] == data["platform"]
    assert content["url"] == data["url"]
    assert content["problem_id"] == data["problem_id"]
    assert content["difficulty"] == data["difficulty"]
    assert content["normalized_difficulty"] == data["normalized_difficulty"]
    assert content["simplified_statement"] == data["simplified_statement"]
    assert content["notes"] == data["notes"]
    assert content["solution_url"] == data["solution_url"]
    assert content["id"] == str(problem.id)


def test_update_problem_not_found(client: TestClient) -> None:
    data: dict = {
        "title": "Updated title",
        "platform": "leetcode",
        "url": "https://leetcode.com/problems/updated-problem",
        "problem_id": "456",
        "difficulty": "hard",
        "normalized_difficulty": 8,
        "simplified_statement": "This is an updated problem statement.",
        "notes": "These are some updated notes.",
        "solution_url": "https://github.com/user/updated-solution",
    }
    response = client.put(
        f"{settings.API_V1_STR}/problems/{uuid.uuid4()}",
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Problem not found"


def test_delete_problem(client: TestClient, db: Session) -> None:
    problem = create_random_problem(db)
    response = client.delete(
        f"{settings.API_V1_STR}/problems/{problem.id}",
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Problem deleted successfully"


def test_delete_problem_not_found(
    client: TestClient,
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/problems/{uuid.uuid4()}",
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Problem not found"
