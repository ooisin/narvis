import logging

from sqlmodel import Session
from backend.app.core.db import engine, init_db


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # File handler to save logs to app.log
        logging.StreamHandler()  # Stream handler to output logs to console
    ]
)

logger = logging.getLogger(__name__)

logger.info("This is an info message.")

def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()