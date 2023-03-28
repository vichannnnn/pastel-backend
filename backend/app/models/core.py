from typing import List, Tuple
from app.db.base_class import Base
from app.schemas.core import PastelImage
from sqlalchemy import Column, Integer, String, select, func
from sqlalchemy.ext.asyncio import AsyncSession
import base64


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
    async def get(
        cls, session: AsyncSession, id: int
    ) -> PastelImage:  # pylint: disable=redefined-builtin,invalid-name
        stmt = select(PastelArt).where(PastelArt.id == id)
        res = await session.execute(stmt)
        return res.scalars().one()

    @classmethod
    async def get_all(
        cls, page: int, size: int, session: AsyncSession
    ) -> Tuple[List[PastelImage], int]:
        stmt = (
            select(
                PastelArt.row_id,
                PastelArt.prompt,
                PastelArt.neg_prompt,
                PastelArt.width,
                PastelArt.height,
                PastelArt.steps,
                PastelArt.guidance,
                PastelArt.image,
                PastelArt.seed,
                func.count(PastelArt.row_id).over().label("total"),
            )
            .limit(size)
            .offset((page * size) - size)
        )
        res = await session.execute(stmt)
        pastel_images_data = res.fetchall()
        pastel_images = [PastelImage(**dict(i)) for i in pastel_images_data]
        total = pastel_images_data[0]["total"] if pastel_images_data else 0
        return pastel_images, total
