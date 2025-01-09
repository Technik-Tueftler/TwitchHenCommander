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


class Link(Base):
    """Class to be able to map the twitch user links via an ORM

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "links"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[User] = relationship(back_populates="links")

    def __repr__(self) -> str:
        return f"Link: {self.id}"


class Video(Base):
    """Class to be able to map the videos via an ORM

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(primary_key=True)
    video_id: Mapped[str] = mapped_column(nullable=False)
    portal: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"Video: {self.video_id}"


class Stream(Base):
    """Class to collect all stream related information

    Args:
        Base (_type_): Basic class that is inherited
    """

    __tablename__ = "streams"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp_start: Mapped[datetime] = mapped_column(nullable=False)
    timestamp_end: Mapped[datetime] = mapped_column(nullable=True)
    hashtags: Mapped[str] = mapped_column(nullable=True)
    chatter: Mapped[str] = mapped_column(nullable=True)


class StreamValidation:
    """Helper class to verify the last streams if a stream message is allowed
    """
    def __init__(self, curr, last):
        self.curr_stream = curr
        self.last_stream = last
        self.no_first_stream = self.last_stream is None


session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def sync_db():
    """Function to run the sync command and create all DB dependencies and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_twitch_user(user_id: str, user_name: str) -> User | None:
    """
    Function searches in DB for twitch user ID and returns the mapped user.
    If the user does not exist, one is created.

    Args:
        user_id (str): Twitch ID of user

    Returns:
        User: User mapped object
    """
    async with session() as sess:
        statement = select(User).where(User.twitch_user_id == user_id)
        result_user = (await sess.execute(statement)).scalar_one_or_none()
        if result_user is None:
            user = User(twitch_user_id=user_id, twitch_user_name=user_name)
            sess.add(user)
            await sess.commit()
            result_user = user
        return result_user


async def get_stream(stream_id: int) -> Stream:
    """Function searches in DB for Stream ID and returns the mapped user

    Args:
        stream_id (int): Stream ID

    Returns:
        Stream: Stream mapped object
    """
    async with session() as sess:
        statement = select(Stream).where(Stream.id == stream_id)
        result = await sess.execute(statement)
    return result.scalar_one_or_none()


async def update_stream(stream_id: int, stream_data: dict) -> None:
    """Function update all transfered stream data

    Args:
        stream_id (int): Stream id to update object
        stream_data (dict): Stream data for update
    """
    async with session() as sess:
        stream = (
            await sess.execute(select(Stream).where(Stream.id == stream_id))
        ).scalar_one_or_none()
        for key, value in stream_data.items():
            if hasattr(stream, key):
                setattr(stream, key, value)
        await sess.commit()


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


async def add_data(data: Stream | Clip | Video) -> int:
    """Add data object to db

    Args:
        stream (Stream): Stream mapped object with necessary

    Returns:
        int: ID from commited object
    """
    async with session() as sess:
        sess.add(data)
        await sess.commit()
        return data.id


async def add_all_data(data: set) -> None:
    """Add set of data to db

    Args:
        data (set): Set of data

    Returns:
        int: ID from commited object
    """
    async with session() as sess:
        sess.add_all(data)
        await sess.commit()


async def last_streams_for_validation_stream_start() -> StreamValidation:
    """Helper function to get the last valid streams. This is for validation 
    if a new stream message is allowed.

    Returns:
        StreamValidation: Stream validation class with information if last streams
    """
    async with session() as sess:
        statement = select(Stream).order_by(Stream.timestamp_start.desc())
        streams = (await sess.execute(statement)).scalars().all()
        if len(streams) < 2:
            return StreamValidation(None, None)
        curr_stream = streams[0]
        last_stream = streams[1]
    return StreamValidation(curr_stream, last_stream)


async def last_video(portal: str) -> Video:
    """
    Function return the last stored video.

    Args:
        portal (str): The portal to be searched

    Returns:
        Video: ID from the last video
    """
    async with session() as sess:
        statement = select(Video).filter(Video.portal == portal).order_by(Video.timestamp.desc())
        video = (await sess.execute(statement)).first()
    if video is None:
        return None
    return video[0]


async def async_main():
    """Scheduling function for regular call."""
    await sync_db()
    # await fetch_last_clip_ids()
    # await get_twitch_user("1234")
    # await get_twitch_user("123333334")
    # user = await add_new_user("77890", "MrT")
    # print(user)
    # temp = await get_twitch_user("77890")
    # print(f"geladener User: {temp}")
    # async with session() as sess:
    #     user = User(twitch_user_id="jhedej", twitch_user_name="Jojo")
    #     sess.add(user)
    #     await sess.commit()
    # print(user.id)
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
    async with session() as sess:
        statement = select(Stream).order_by(Stream.timestamp_start.desc())
        streams = (await sess.execute(statement)).scalars().all()
        curr_stream = streams[0]
        last_stream = streams[1]
        refer_stream = streams[1]
        print(f"start id: {curr_stream.id}")
        print(f"last id: {last_stream.id}")
        #print(last_stream.timestamp_end)
        print(f"Anzahl: {len(streams)}")
        if last_stream.timestamp_end is None:
            for stream in streams[2:]:
                #print(stream.timestamp_end)
                if stream.timestamp_end is not None:
                    refer_stream = stream
                    break
                #print(stream.id, stream.timestamp_start, stream.timestamp_end)
        print(f"ref id: {refer_stream.id}")


if __name__ == "__main__":
    asyncio.run(async_main())
