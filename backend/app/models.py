import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import ClassVar

from pydantic import field_validator
from sqlalchemy import DateTime
from sqlmodel import CheckConstraint, Field, Index, SQLModel, UniqueConstraint


def get_datetime_utc() -> datetime:
    return datetime.now(UTC)


class ProblemPlatform(StrEnum):
    leetcode = "leetcode"
    hackerrank = "hackerrank"


class ProblemDifficulty(StrEnum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


# Shared properties
class ProblemBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    platform: ProblemPlatform = Field(index=True)
    url: str = Field(min_length=1, max_length=2048)
    problem_id: str | None = Field(default=None, min_length=1, max_length=100)
    difficulty: ProblemDifficulty = Field(index=True)
    normalized_difficulty: int | None = Field(
        default=None,
        ge=1,
        le=10,
        index=True,
    )
    simplified_statement: str | None = Field(default=None, max_length=10_000)
    notes: str | None = Field(default=None, max_length=10_000)
    solution_url: str | None = Field(default=None, max_length=2048)

    @field_validator("title", "problem_id", mode="before")
    @classmethod
    def strip_required_text(cls, value: object) -> object:
        return value.strip() if isinstance(value, str) else value

    @field_validator("simplified_statement", "notes", mode="before")
    @classmethod
    def normalize_optional_text(cls, value: object) -> object:
        if not isinstance(value, str):
            return value
        return value.strip() or None


# Properties to receive on item creation
class ProblemCreate(ProblemBase):
    pass


# Database model
class Problem(ProblemBase, table=True):
    __table_args__: ClassVar[tuple[CheckConstraint | UniqueConstraint | Index, ...]] = (
        CheckConstraint(
            "normalized_difficulty IS NULL OR normalized_difficulty BETWEEN 1 AND 10",
            name="ck_problem_normalized_difficulty_range",
        ),
        UniqueConstraint(
            "platform",
            "problem_id",
            name="uq_problem_platform_problem_id",
        ),
        Index(
            "ix_problem_platform_difficulty",
            "platform",
            "difficulty",
        ),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )
    updated_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # type: ignore
    )


# Properties to return via API
class ProblemPublic(ProblemBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProblemsPublic(SQLModel):
    data: list[ProblemPublic]
    count: int
