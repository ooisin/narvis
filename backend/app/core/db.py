from sqlmodel import Session, create_engine, select, SQLModel

from backend.app.core.config import settings
from backend.app.crud import crud
from backend.app.models.models import User, UserCreate

engine = create_engine(str(settings.DATABASE_URI), echo=True)


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)

    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)