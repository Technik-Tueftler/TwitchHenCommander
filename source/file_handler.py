"""
All functions to provide reading and saving for important data over the program runtime
"""
import asyncio
from pathlib import Path
import json
from datetime import datetime
import aiofiles
from constants import CACHE_FILE_PATH, TIMESTAMP_PATTERN, DEFAULT_CACHE_DATA


async def load_cache_data() -> dict:
    """Load the cache data from path and return

    Returns:
        dict: Cache data 
    """
    if not Path(CACHE_FILE_PATH).exists():
        async with aiofiles.open(CACHE_FILE_PATH, "w") as file:
            await file.write(json.dumps(DEFAULT_CACHE_DATA))
        return DEFAULT_CACHE_DATA
    try:
        async with aiofiles.open(CACHE_FILE_PATH, "r") as file:
            content = json.loads(await file.read())
        return content
    except json.JSONDecodeError as _:
        return DEFAULT_CACHE_DATA

async def load_last_clip_timestamp() -> datetime:
    """Read the last fetched timestamp from file for the clip feature

    Returns:
        datetime: Last fetched timestamp
    """
    data = await load_cache_data()
    if "clip_last_timestamp" in data:
        return datetime.strptime(data["clip_last_timestamp"], TIMESTAMP_PATTERN)
    return datetime.strptime(DEFAULT_CACHE_DATA["clip_last_timestamp"], TIMESTAMP_PATTERN)


async def save_cache_data(data_to_save: dict) -> None:
    """Save new or updated data to cach file

    Args:
        data_to_save (dict): Data to be stored
    """
    data = DEFAULT_CACHE_DATA.copy()
    data.update(await load_cache_data())
    data.update(data_to_save)
    async with aiofiles.open(CACHE_FILE_PATH, "w") as file:
        await file.write(json.dumps(data))


if __name__ == "__main__":
    # asyncio.run(load_last_clip_timestamp())
    # asyncio.run(save_cache_data({"clip_last_timestamp2": "2020-02-02T12:00:00Z"}))
    asyncio.run(load_last_clip_timestamp())
