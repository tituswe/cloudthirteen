from sqlalchemy.orm import Session

__all__ = ['BaseRepo']


class BaseRepo:
    """Base repository for handling database session binding."""

    def __init__(self, session: Session):
        self.session = session
        self.engine = session.bind

    def close(self):
        """Close the database session."""
        self.session.close()
