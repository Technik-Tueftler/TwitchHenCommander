"""
All functions to provide reading and saving for important data over the program runtime
"""
import asyncio
import json
from datetime import datetime
import aiofiles
from constants import CONFIGURATION_FILE_PATH


async def load_last_clip_timestamp() -> datetime:
    """Read the last fetched timestamp from file for the clip feature

    Returns:
        datetime: Last fetched timestamp
    """
    async with aiofiles.open(CONFIGURATION_FILE_PATH, "r") as file:
        content = await file.read()
        string_timestamp = json.loads(content)["clips"]["clip_last_timestamp"]
        timestamp = datetime.strptime(string_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    return timestamp


if __name__ == "__main__":
    asyncio.run(load_last_clip_timestamp())
