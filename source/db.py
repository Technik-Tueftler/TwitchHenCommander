"""All functions and handler for db access
"""

import asyncio
from datetime import datetime, timedelta
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


async def add_user():
    async with engine.begin():
        async with session() as sess:
            sess.add(
                User(
                    twitch_user_id="5678",
                    twitch_user_name="Kinger",
                    clips = [
                        Clip(
                            clip_id="ujkhegfdeue3e",
                            timestamp=datetime.utcnow(),
                            title="Super cooles Huhn"
                        ),
                        Clip(
                            clip_id="ujkhegfddepdkeeue3e",
                            timestamp=datetime.utcnow(),
                            title="Super super cooles Huhn"
                        ),
                        Clip(
                            clip_id="peuoifdteiugfe444",
                            timestamp=datetime.utcnow(),
                            title="Geniales cooles Huhn"
                        )
                    ]
                )
            )
            await sess.commit()


async def fetch_last_clip_ids():
    timestamp = datetime.utcnow()
    seconds = 600 # UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")
    async with session() as sess:
        statement = select(Clip).where(
            Clip.timestamp < start_timestamp
        )
        result = await sess.execute(statement)
    return result.scalars().all()


async def async_main():
    await sync_db()
    await fetch_last_clip_ids()


if __name__ == "__main__":
    asyncio.run(async_main())
