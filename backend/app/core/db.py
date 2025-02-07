from sqlmodel import Session, create_engine, select, SQLModel

from backend.app.core.config import settings

engine = create_engine(str(settings.DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
    # TODO: Insert all user logic checks - create if not in db