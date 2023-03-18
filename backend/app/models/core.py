import collections
from datetime import date, timedelta
from typing import TYPE_CHECKING, Any, Dict, List
from app.db.base_class import Base
from app.exceptions import AppError
from sqlalchemy import exc as SQLAlchemyExceptions
from sqlalchemy import Column, ForeignKey, Table, UniqueConstraint
from sqlalchemy import ARRAY, Boolean, DateTime, Integer, String
from sqlalchemy import or_, select, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.sql.expression import func
from app.schemas.core import PastelPrompt, PastelImage, PromptType


class PastelArt(Base):
    __tablename__ = "pastel_art"
    row_id = Column(Integer, primary_key=True, nullable=False)
    prompt = Column(String, unique=True, nullable=False)
    negative_prompt = Column(String, unique=True, nullable=False)
    width = Column(Integer, unique=True, nullable=False)
    height = Column(Integer, unique=True, nullable=False)
    steps = Column(Integer, unique=True, nullable=False)
    guidance = Column(Integer, unique=True, nullable=False)
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

    #
    # @classmethod
    # async def get_all(
    #     cls, session: AsyncSession
    # ) -> List[TrainStationWithConnectionSchema]:
    #     res = await session.execute(
    #         select(Station).options(selectinload(Station.connecting_stations))
    #     )
    #     return res.scalars().all()
    #
    # @classmethod
    # async def update_by_id(
    #     cls, session: AsyncSession, id: str, data: TrainStationSchema
    # ) -> TrainStationWithConnectionSchema:
    #
    #     stmt = (
    #         update(Station)
    #         .returning(literal_column("*"))
    #         .where(Station.id == id)
    #         .values(**dict(data))
    #     )
    #     await session.execute(stmt)
    #     await session.commit()
    #     result = await Station.get(session=session, id=data.id)
    #     # result = TrainStationWithConnectionSchema.from_orm(res.fetchone())
    #     return result
