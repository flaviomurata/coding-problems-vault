from fastapi import APIRouter
from sqlmodel import col, func, select

from app.api.deps import SessionDep
from app.models import Problem, ProblemPublic, ProblemsPublic

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
