import asyncio
from typing import AsyncGenerator
import ast

from app.api.deps import get_session
from app.login import Authenticator
from app.main import app
from app.db.base_class import Base

# from app.models.core import PostData
from app import models
from app import schemas

from fastapi.testclient import TestClient
from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from faker import Faker
import pytest


SQLALCHEMY_DATABASE_URL = PostgresDsn.build(
    scheme="postgresql+asyncpg",
    user="postgres",
    password="postgres",
    host="db",
    port="5432",
    path="/test",
)

test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, future=True, poolclass=NullPool
)
TestingSessionLocal = sessionmaker(
    test_engine, autoflush=False, expire_on_commit=False, class_=AsyncSession
)


async def init_models():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


asyncio.run(init_models())


async def override_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
        await session.close()


app.dependency_overrides[get_session] = override_session


@pytest.fixture(name="test_authentication_client", scope="function")
def test_authentication_client():
    yield TestClient(app)


@pytest.fixture(name="not_authenticated_client", scope="function")
def not_authenticated_client():
    app.dependency_overrides = {get_session: override_session}
    yield TestClient(app)


@pytest.fixture(name="client", scope="function")
def fixture_client():
    class User:
        def __init__(self):
            self.username = "test"

    def skip():
        pass

    def skip_user():
        return User()

    app.dependency_overrides[Authenticator.verify] = skip
    app.dependency_overrides[Authenticator.get_current_user] = skip_user
    with TestClient(app) as client:
        yield client


# Fixtures for data_source table, named ds for short. This allows modification of pytest's parameters for ds.
fake = Faker()


@pytest.fixture()
def ds_game() -> str:  # type: ignore
    yield "Echocalypse"


@pytest.fixture()
def ds_platform() -> str:  # type: ignore
    yield "Twitter"


@pytest.fixture()
def ds_country() -> str:  # type: ignore
    yield "Japan (xxxx)"


@pytest.fixture()
def ds_author_name() -> str:  # type: ignore
    yield fake.name()


@pytest.fixture()
def ds_content() -> str:  # type: ignore
    yield fake.sentence()


@pytest.fixture()
def ds_post_date() -> str:  # type: ignore
    yield fake.date()


@pytest.fixture()
def ds_platform_data() -> str:  # type: ignore
    yield ast.literal_eval(
        '{"user_id": "418407066", "hyperlink": "https://taptap.io/post/1783023", "user_rating": 2}'
    )


@pytest.fixture()
def ds_processed() -> str:  # type: ignore
    yield True


@pytest.fixture()
def ds_detected_language() -> str:  # type: ignore
    yield fake.word()


@pytest.fixture()
def ds_parsed_content() -> str:  # type: ignore
    yield fake.sentence()


@pytest.fixture()
def ds_ai_data() -> str:  # type: ignore
    yield ast.literal_eval('{"label": "negative", "probability": 0.4809485673904419}')


@pytest.fixture
def populate_test_db(
    ds_game: str,
    ds_platform: str,
    ds_country: str,
    ds_author_name: str,
    ds_content: str,
    ds_post_date: str,
    ds_platform_data: str,
    ds_processed: bool,
    ds_detected_language: str,
    ds_parsed_content: str,
    ds_ai_data: dict,
):
    yield models.core.PostData(
        game=ds_game,
        platform=ds_platform,
        country=ds_country,
        author_name=ds_author_name,
        content=ds_content,
        post_date=ds_post_date,  # type: ignore
        platform_data=ds_platform_data,
        processed=ds_processed,
        detected_language=ds_detected_language,
        parsed_content=ds_parsed_content,
        ai_data=ds_ai_data,
    )


# Authentication
@pytest.fixture()
def correct_login_user():
    yield schemas.authentication.UserSchema(username="username", password="password")


@pytest.fixture()
def wrong_login_user():
    yield schemas.authentication.UserSchema(
        username="wrongusername", password="wrongpassword"
    )


# Core

# tag
@pytest.fixture()
def tag():
    yield schemas.tags.TagSchema(
        tag_name="string", color="#DAF625", bg="#dDE", keywords=["string"]
    )


# Stats

# follower_stat_time
@pytest.fixture()
def follower_stat_time() -> str:  # type: ignore
    yield ["2001-12-1", "2001-12-5"]


@pytest.fixture()
def follower_stat(follower_stat_time):
    yield schemas.follower_count.FollowerCountGetQuery(
        platforms="", games="", countries="", time=follower_stat_time
    )
