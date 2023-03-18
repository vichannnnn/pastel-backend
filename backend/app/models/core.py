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
