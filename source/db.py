"""All functions and handler for db access
"""

import asyncio
from datetime import datetime, timedelta, UTC
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import environment_verification as env

engine = create_async_engine("sqlite+aiosqlite:///../files/HenCommander.db", echo=False)


class Base(DeclarativeBase):
    """Declarative base class

    Args:
        DeclarativeBase (_type_): Basic class that is inherited
    """


class User(Base):
    """Class to be able to map the twitch user via an ORM

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    twitch_user_id: Mapped[str] = mapped_column(nullable=False)
    twitch_user_name: Mapped[str] = mapped_column(nullable=False)
    clips: Mapped[List["Clip"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User: {self.twitch_user_name}"


class Clip(Base):
    """Class to be able to map the twitch user clips via an ORM

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "clips"
    id: Mapped[int] = mapped_column(primary_key=True)
    clip_id: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[User] = relationship(back_populates="clips")

    def __repr__(self) -> str:
        return f"Clip: {self.clip_id}"


class Stream(Base):
    """Class to collect all stream related information

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "streams"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    hashtags: Mapped[str] = mapped_column(nullable=True)
    chatter: Mapped[str] = mapped_column(nullable=True)


session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def sync_db():
    """Function to run the sync command and create all DB dependencies and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_twitch_user(user_id: str) -> User:
    """Function searches in DB for twitch user ID and returns the mapped user

    Args:
        user_id (str): Twitch ID of user

    Returns:
        User: User mapped object
    """
    async with session() as sess:
        statement = select(User).where(User.twitch_user_id == user_id)
        result = await sess.execute(statement)
    return result.scalar_one_or_none()


async def add_new_user(twitch_user_id: str, twitch_user_name: str) -> User:
    """Create a new entry in DB for user

    Args:
        twitch_user_id (str): Twitch user ID
        twitch_user_name (str): Twitch user name

    Returns:
        User: User mapped object
    """
    async with session() as sess:
        user = User(twitch_user_id=twitch_user_id, twitch_user_name=twitch_user_name)
        sess.add(user)
        await sess.commit()
    return user


async def fetch_last_clip_ids() -> List[int]:
    """Function gets all the clips in the last time period

    Returns:
        List[int]: List of clip IDs
    """
    timestamp = datetime.now(UTC)
    seconds = env.app_settings["clips_fetch_time"]
    start_timestamp = (timestamp - timedelta(seconds=seconds)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    async with session() as sess:
        statement = select(Clip).where(Clip.timestamp < start_timestamp)
        result = await sess.execute(statement)
        all_clips = result.scalars().all()
    return [clip.clip_id for clip in all_clips]


async def add_data(data: Stream | Clip) -> None:
    """Add data object to db

    Args:
        stream (Stream): Stream mapped object with necessary
    """
    async with session() as sess:
        sess.add(data)
        await sess.commit()


async def async_main():
    """Scheduling function for regular call."""
    await sync_db()
    # await fetch_last_clip_ids()
    # await get_twitch_user("1234")
    # await get_twitch_user("123333334")
    # user = await add_new_user("77890", "MrT")
    # print(user)
    temp = await get_twitch_user("77890")
    print(f"geladener User: {temp}")
    async with session() as sess:
        user = User(twitch_user_id="jhedej", twitch_user_name="Jojo")
        sess.add(user)
        await sess.commit()
    print(user.id)
    # statement = select(User).where(User.twitch_user_id == temp.twitch_user_id)
    # result = await sess.execute(statement)
    # checked_user = result.scalar_one()
    # checked_user.twitch_user_name = "MrZ"
    # sess.add(
    #     Clip(
    #         user_id=checked_user.id,
    #         clip_id="fuuuu",
    #         timestamp=datetime.now(UTC),
    #         title="Super cooles Fliegerhuhn",
    #     )
    # )
    # await sess.commit()

    # temp.twitch_user_name = "MrY"
    # await sess.commit()


if __name__ == "__main__":
    asyncio.run(async_main())
