import random

from sqlmodel import Session

from app import crud
from app.models import Problem, ProblemCreate, ProblemPlatform
from tests.utils.utils import random_integer, random_lower_string


def create_random_problem(db: Session) -> Problem:
    title = random_lower_string()
    platform = (
        ProblemPlatform.leetcode
        if random_lower_string() < "m"
        else ProblemPlatform.hackerrank
    )
    problem_id = str(random_integer(1, 4000))
    url = f"https://{platform.value}.com/problems/{random_lower_string()}"
    difficulty = random.choice(["easy", "medium", "hard"])
    normalized_difficulty = random_integer(1, 10)
    simplified_statement = random_lower_string()
    notes = random_lower_string()
    problem_in = ProblemCreate(
        title=title,
        platform=platform,
        url=url,
        problem_id=problem_id,
        difficulty=difficulty,
        normalized_difficulty=normalized_difficulty,
        simplified_statement=simplified_statement,
        notes=notes,
    )
    return crud.create_problem(session=db, problem_in=problem_in)
