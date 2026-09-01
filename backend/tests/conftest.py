from collections.abc import Generator

import pytest
from app.core.db import engine
from app.main import app
from app.models import Problem
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, delete


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session]:
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

        statement = delete(Problem)
        session.exec(statement)
        session.commit()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient]:
    with TestClient(app) as c:
        yield c
