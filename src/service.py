from sqlalchemy.orm import Session
from src.data import Snipper, engine


class SnipperService:
    def __init__(self):
        """
        Initialize SnipperService
        """
        self.session = Session(engine)

    def get_snipper(self, snipper_id):
        """
        Get snipper by id

        Args:
        snipper_id: str: Snipper id

        Returns:
        Snipper: Snipper object
        """
        return (
            self.session.query(Snipper)
            .filter(Snipper.id == snipper_id)
            .first()
        )

    def create_snipper(self, url, ip):
        """
        Create snipper

        Args:
        url: str: Snipper url
        ip: str: Snipper ip

        Returns:
        Snipper: Snipper object
        """
        snipper = Snipper(url=url, ip=ip)
        self.session.add(snipper)
        self.session.commit()
        return snipper

    def delete_snipper(self, snipper_id):
        snipper = self.get_snipper(snipper_id)
        self.session.delete(snipper)
        self.session.commit()

    def get_all_snippers(self):
        """
        Get all snippers

        Returns:
        list: List of Snipper objects
        """
        return self.session.query(Snipper).all()

    def __del__(self):
        self.session.close()
