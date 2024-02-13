import aiofiles
import asyncio
import json
from datetime import datetime
from constants import CONFIGURATION_FILE_PATH


async def load_last_clip_timestamp() -> datetime.datetime:
    async with aiofiles.open(CONFIGURATION_FILE_PATH, "r") as file:
        content = await file.read()
        timestamp = datetime.strftime(
            json.loads(content)["clips"]["clip_last_timestamp"], "%Y-%m-%dT%H:%M:%SZ"
        )
    return timestamp


if __name__ == "__main__":
    asyncio.run(load_last_clip_timestamp())
