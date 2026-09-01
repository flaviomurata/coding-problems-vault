from sqlmodel import Session

from app.models import Problem, ProblemCreate


def create_problem(*, session: Session, problem_in: ProblemCreate) -> Problem:
    db_problem = Problem.model_validate(problem_in)
    session.add(db_problem)
    session.commit()
    session.refresh(db_problem)
    return db_problem
