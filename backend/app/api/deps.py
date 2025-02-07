from typing import Annotated
from collections import Generator

from fastapi import Depends
from sqlmodel import Session

from backend.app.core import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]