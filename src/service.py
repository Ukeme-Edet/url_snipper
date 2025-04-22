from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.data import Snipper, engine


class SnipperService:
    def __init__(self):
        """
        Initialize SnipperService
        """

    async def get_snipper_by_id(self, snipper_id):
        """
        Get snipper by id

        Args:
        snipper_id: str: Snipper id

        return:
        Snipper: Snipper object
        """
        async with AsyncSession(engine) as session:
            result = await session.execute(
                select(Snipper).where(Snipper.id == snipper_id)
            )
            return result.scalars().first()

    async def get_snipper_by_url(self, url):
        """
        Get snipper by url

        Args:
        url: str: Snipper url

        return:
        Snipper: Snipper object
        """
        async with AsyncSession(engine) as session:
            result = await session.execute(
                select(Snipper).where(Snipper.url == url)
            )
            return result.scalars().first()

    async def create_snipper(self, url, ip):
        """
        Create snipper

        Args:
        url: str: Snipper url
        ip: str: Snipper ip

        return:
        Snipper: Snipper object
        """
        async with AsyncSession(engine) as session:
            snipper = Snipper(url=url, ip=ip)
            session.add(snipper)
            await session.commit()
            await session.refresh(snipper)
            return snipper

    async def delete_snipper(self, snipper_id):
        async with AsyncSession(engine) as session:
            snipper = await self.get_snipper_by_id(snipper_id)
            if snipper:
                await session.delete(snipper)

    async def get_all_snippers(self):
        """
        Get all snippers

        return:
        list: List of Snipper objects
        """
        async with AsyncSession(engine) as session:
            result = await session.execute(select(Snipper))
            return result.scalars().all()
