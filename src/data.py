from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, create_engine
from datetime import datetime, timedelta

from src.utils import generate_url_key


class Base(DeclarativeBase):
    """
    Base class for all models
    """

    pass


class Snipper(Base):
    """
    Snipper model

    Attributes:
    id: str: Snipper id
    url: str: Snipper url
    ip: str: Snipper ip
    date_created: datetime: Snipper creation date
    delete_date: datetime: Snipper deletion date
    """

    __tablename__ = "snippers"
    id = Column(String, primary_key=True, nullable=False)
    url = Column(String, nullable=False, unique=True)
    ip = Column(String, nullable=False)
    date_created = Column(String, default=datetime.now)
    delete_date = Column(String, default=datetime.now() + timedelta(weeks=8))

    def __init__(self, url: str, ip: str):
        """
        Initialize Snipper

        Args:
        url: str: Snipper url
        ip: str: Snipper ip
        """
        self.id = generate_url_key()
        self.url = url
        self.ip = ip

    def __repr__(self):
        """
        String representation of Snipper

        Returns:
        str: Snipper representation
        """
        return f"<Snipper(id={self.id!r}, url={self.url!r})>"


engine = create_engine("sqlite:///snippers.db")
Base.metadata.create_all(engine)
