"""All functions and features that work with the help of the twitch api
"""

from datetime import datetime, timedelta, UTC
from string import Template

import asyncio
import requests
import db
import hashtag_handler as hashh
from constants import (
    REQUEST_TIMEOUT,
    CLIP_WAIT_TIME,
    TIMESTAMP_PATTERN,
)
from watcher import logger


class MyTemplate(Template):
    """This class allow the creation of a template with a user defined separator.
    The package is there to define templates for texts and then substitute them with certain values.
    Args:
        Template (_type_): Basic class that is inherited
    """

    delimiter = "#"


@logger.catch
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
    seconds = settings["clips_fetch_time"]
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
    response_temp = requests.get(fetch_url, headers=headers, timeout=REQUEST_TIMEOUT)
    response = response_temp.json()
    limit = response_temp.headers.get("Ratelimit-Limit")
    remaining = response_temp.headers.get("Ratelimit-Remaining")
    reset_time = response_temp.headers.get("Ratelimit-Reset")
    logger.info(
        f"Fetch new clips with: Limit: {limit} / Remaining: {remaining} / Reset Time: {reset_time}"
    )
    return response["data"]


@logger.catch
async def streaming_handler(**settings) -> None:
    """Function check if stream is running or not and set configured interfaces

    Args:
        settings (_type_): App settings
    """
    broadcaster = settings["nickname"]
    client_id = settings["ID"]
    token = settings["token"]
    is_live_url = (
        f"https://api.twitch.tv/helix/search/channels?query="
        f"{broadcaster}&live_only=true"
    )
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    # {"data": [], "pagination": {}}

    # {data": [ {"display_name": "Technik_Tueftler", "game_id": "509658",
    # "game_name": "Just Chatting", "is_live": true,
    # "tags": ["KeinBackseatGaming","Deutsch"], "title": "Reaction",
    # "started_at": "2024-04-02T12:45:22Z"} ],"pagination": {}

    # {'data': [{'display_name': 'Technik_Tueftler', 'game_id': '766571430',
    # 'game_name': 'HELLDIVERS 2', 'id': '206130928', 'is_live': False,
    # 'tags': ['visuellesASMR', 'Deutsch', 'KeineBackseatgaming'],
    # 'title': '🐔 Noch 2 Achievements #34 🐔',
    # 'started_at': ''}], 'pagination': {}}
    response_temp = requests.get(is_live_url, headers=headers, timeout=REQUEST_TIMEOUT)
    response = response_temp.json()
    limit = response_temp.headers.get("Ratelimit-Limit")
    remaining = response_temp.headers.get("Ratelimit-Remaining")
    reset_time = response_temp.headers.get("Ratelimit-Reset")
    logger.info(
        f"Get online status with: Limit: {limit} / "
        + f"Remaining: {remaining} / "
        + f"Reset Time: {reset_time}"
    )
    # print(response)
    if settings["start_bot_at_streamstart"]:
        if (
            response["data"]
            and not hashh.app_data["online"]
            and response["data"][0]["is_live"]
        ):
            await hashh.allow_collecting(True)
    if settings["finish_bot_at_streamend"]:
        if not response["data"] and hashh.app_data["online"]:
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()
        elif (
            response["data"]
            and hashh.app_data["online"]
            and not response["data"][0]["is_live"]
        ):
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()


async def new_clips_handler(**settings) -> None:
    """Handling function to find new clips and then post them"""
    if not settings["database_synchronized"]:
        await db.sync_db()
        settings["database_synchronized"] = True
    clips = await fetch_new_clips(settings)
    last_clip_ids = await db.fetch_last_clip_ids()
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
        await db.add_data(db_clip)

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
