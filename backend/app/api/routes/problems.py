import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import SessionDep
from app.models import Problem, ProblemCreate, ProblemPublic, ProblemsPublic

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("/", response_model=ProblemsPublic)
def read_problems(
    session: SessionDep,
) -> ProblemsPublic:
    """
    Retrieve problems.
    """

    count_statement = select(func.count()).select_from(Problem)
    count = session.exec(count_statement).one()
    statement = select(Problem).order_by(col(Problem.created_at).desc())
    problems = session.exec(statement).all()

    problems_public = [ProblemPublic.model_validate(problem) for problem in problems]
    return ProblemsPublic(data=problems_public, count=count)


@router.get("/{id}", response_model=ProblemPublic)
def read_item(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Get problem by ID.
    """
    problem = session.get(Problem, id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.post("/", response_model=ProblemPublic)
def create_problem(*, session: SessionDep, problem_in: ProblemCreate) -> Any:
    """
    Create new problem.
    """
    problem = Problem.model_validate(problem_in)
    session.add(problem)
    session.commit()
    session.refresh(problem)
    return problem
