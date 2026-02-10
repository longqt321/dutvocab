from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel


class Card(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    word: str = Field(index=True)
    meaning: str
    level: Optional[str] = None
    note: Optional[str] = None

    #SRS - spaced repetition
    repetitions: int = Field(default=0)
    easiness_factor: float = Field(default=0.25)
    interval: float = Field(default=0)

    last_review: date = Field(default_factory=date.today)
    next_review: date = Field(default_factory=date.today)



