"""All functions and handler for db access
"""

import asyncio
from datetime import datetime, timedelta, UTC
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///sample.db", echo=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    twitch_user_id: Mapped[str] = mapped_column(nullable=False)
    twitch_user_name: Mapped[str] = mapped_column(nullable=False)
    clips: Mapped[List["Clip"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User: {self.twitch_user_name}"


class Clip(Base):
    __tablename__ = "clips"
    id: Mapped[int] = mapped_column(primary_key=True)
    clip_id: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(nullable=False)
    user: Mapped[User] = relationship(back_populates="clips")

    def __repr__(self) -> str:
        return f"Clip: {self.clip_id}"


session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def sync_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_twitch_user(user_id: str) -> User:
    async with session() as sess:
        statement = select(User).where(User.twitch_user_id == user_id)
        result = await sess.execute(statement)
    return result.scalar_one_or_none()


async def add_new_user(twitch_user_id: str, twitch_user_name: str) -> User:
    async with session() as sess:
        user = User(twitch_user_id=twitch_user_id, twitch_user_name=twitch_user_name)
        sess.add(user)
        await sess.commit()
    return user


async def add_user():
    async with engine.begin():
        async with session() as sess:
            sess.add(
                User(
                    twitch_user_id="5678",
                    twitch_user_name="Kinger",
                    clips=[
                        Clip(
                            clip_id="ujkhegfdeue3e",
                            timestamp=datetime.utcnow(),
                            title="Super cooles Huhn",
                        ),
                        Clip(
                            clip_id="ujkhegfddepdkeeue3e",
                            timestamp=datetime.utcnow(),
                            title="Super super cooles Huhn",
                        ),
                        Clip(
                            clip_id="peuoifdteiugfe444",
                            timestamp=datetime.utcnow(),
                            title="Geniales cooles Huhn",
                        ),
                    ],
                )
            )
            await sess.commit()


async def fetch_last_clip_ids():
    timestamp = datetime.now(UTC)
    seconds = 600  # UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(seconds=seconds)).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )
    async with session() as sess:
        statement = select(Clip).where(Clip.timestamp < start_timestamp)
        result = await sess.execute(statement)
    return result.scalars().all()


async def add_user_clip(clip: Clip) -> None:
    async with session() as sess:
        sess.add(clip)
        await sess.commit()


async def async_main():
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
