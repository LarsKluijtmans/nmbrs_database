"""Session manager"""

from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker, Session


@contextmanager
def session_scope(session_maker: sessionmaker[Session]):
    """Session manager"""
    session: Session = session_maker()
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()
