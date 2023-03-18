from typing import List
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.core import PastelImage


class PastelArt(Base):
    __tablename__ = "pastel_art"
    row_id = Column(Integer, primary_key=True, nullable=False)
    prompt = Column(String, nullable=False)
    neg_prompt = Column(String, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    guidance = Column(Integer, nullable=False)
    seed = Column(Integer, nullable=False)
    image = Column(String, unique=True, nullable=False)

    async def insert(self, session: AsyncSession) -> PastelImage:
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return PastelImage(**self.__dict__)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> PastelImage:
        stmt = select(PastelArt).where(PastelArt.id == id)
        res = await session.execute(stmt)
        return res.scalars().one()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[PastelImage]:
        res = await session.execute(select(PastelArt))
        return res.scalars().all()
