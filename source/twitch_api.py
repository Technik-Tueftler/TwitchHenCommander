"""All functions and features that work with the help of the twitch api
"""

from datetime import datetime, timedelta, UTC
from string import Template

import asyncio
import requests
import db
from constants import (
    REQUEST_TIMEOUT,
    UPDATE_INTERVAL_PUBLISH_NEW_CLIPS,
    CLIP_WAIT_TIME,
    TIMESTAMP_PATTERN,
)

class MyTemplate(Template):
    """This class allow the creation of a template with a user defined separator.
    The package is there to define templates for texts and then substitute them with certain values.
    Args:
        Template (_type_): Basic class that is inherited
    """
    delimiter = "#"

async def fetch_new_clips(settings) -> list:
    """Function to find new clips in the last interval

    Args:
        settings (dict): App settings

    Returns:
        list: List of all clips in last interval
    """
    broadcaster_id = settings["broadcaster_id"]
    client_id = settings["ID"]
    token = settings["token"]
    timestamp = datetime.now(UTC)
    seconds = UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(seconds=seconds)).strftime(
        TIMESTAMP_PATTERN
    )
    end_timestamp = timestamp.strftime(TIMESTAMP_PATTERN)
    fetch_url = (
        f"https://api.twitch.tv/helix/clips?"
        f"broadcaster_id={broadcaster_id}&"
        f"started_at={start_timestamp}&"
        f"ended_at={end_timestamp}"
    )
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    # {'error': 'Not Found', 'status': 404, 'message': ''}
    response = requests.get(fetch_url, headers=headers, timeout=REQUEST_TIMEOUT).json()
    return response["data"]


async def new_clips_handler(**settings) -> None:
    """Handling function to find new clips and then post them"""
    if not settings["database_synchronized"]:
        await db.sync_db()
        settings["database_synchronized"] = True
    clips = await fetch_new_clips(settings)
    last_clip_ids = (
        await db.fetch_last_clip_ids()
    )
    new_clips = [clip for clip in clips if clip["id"] not in last_clip_ids]
    if not new_clips:
        return
    for clip in new_clips:
        user = await db.get_twitch_user(clip["creator_id"])
        if user is None:
            user = await db.add_new_user(clip["creator_id"], clip["creator_name"])
        db_clip = db.Clip(
            user_id=user.id,
            clip_id=clip["id"],
            timestamp=datetime.strptime(clip["created_at"], TIMESTAMP_PATTERN),
            title=clip["title"],
        )
        await db.add_user_clip(db_clip)

        content = MyTemplate(settings["clip_thank_you_text"]).substitute(
            link=clip["url"], user=clip["creator_name"]
        )
        await post_clips(settings, content)
        await asyncio.sleep(CLIP_WAIT_TIME)


async def post_clips(settings: dict, content: str) -> None:
    """Post clip in discord with all information

    Args:
        settings (dict): Settings to get access to descord webhook
        content (str): Clip link with user information
    """
    if not settings["dc_feature_clips"]:
        return
    data = {"content": content, "username": settings["discord_username_clip"]}
    requests.post(settings["webhook_url_clip"], data=data, timeout=REQUEST_TIMEOUT)


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
