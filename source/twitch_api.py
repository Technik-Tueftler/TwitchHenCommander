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
from generic_functions import generic_http_request
from watcher import logger


class MyTemplate(Template):
    """This class allow the creation of a template with a user defined separator.
    The package is there to define templates for texts and then substitute them with certain values.
    Args:
        Template (_type_): Basic class that is inherited
    """

    delimiter = "#"


def log_ratelimit(debug_level: str, response: requests.models.Response):
    """Log ratelimits for twitch API

    Args:
        debug_level (str): log level from settings
        response (requests.models.Response): response from request
    """
    if debug_level != "DEBUG":
        return
    limit = response.headers.get("Ratelimit-Limit", "NA")
    remaining = response.headers.get("Ratelimit-Remaining")
    reset_time = response.headers.get("Ratelimit-Reset")
    logger.debug(
        f"Get online status with: Limit: {limit} / "
        f"Remaining: {remaining} / "
        f"Reset Time: {reset_time}"
    )


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
    response_temp = await generic_http_request(fetch_url, headers, logger=logger)
    if response_temp is None:
        return None
    log_ratelimit(settings["log_level"], response_temp)
    response = response_temp.json()
    return response["data"]


async def check_stream_start_message(settings: dict, response: dict) -> None:
    """Check if feature active and call the right method for stream start message

        Args:
        settings (dict): _description_
        response (dict): _description_
    """
    if settings["dc_feature_start_message"] and not hashh.app_data["start_message_done"]:
        if (
            response["data"]
            and response["data"][0]["is_live"]
        ):
            await hashh.stream_start_message()
            async with hashh.lock:
                hashh.app_data["start_message_done"] = True
            logger.debug("Send Stream-Start Message to discord")
    elif settings["dc_feature_start_message"] and hashh.app_data["start_message_done"]:
        # ToDo: hier gehts weiter
        ...


async def check_stream_start(settings: dict, response: dict) -> None:
    """_summary_

    Args:
        settings (dict): _description_
        response (dict): _description_
    """
    if settings["start_bot_at_streamstart"]:
        if (
            response["data"]
            and not hashh.app_data["online"]
            and response["data"][0]["is_live"]
        ):
            await hashh.allow_collecting(True)
            await hashh.set_stream_status(True)
            logger.debug("Automatic Stream-Start detected, collecting hashtags allowed.")


async def check_stream_end(settings: dict, response: dict) -> None:
    """_summary_

    Args:
        settings (dict): _description_
        response (dict): _description_
    """
    if settings["finish_bot_at_streamend"]:
        if not response["data"] and hashh.app_data["online"]:
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()
            await hashh.set_stream_status(False)
            logger.debug("Automatic Stream-End (1) detected, hashtags puplished.")
        elif (
            response["data"]
            and hashh.app_data["online"]
            and not response["data"][0]["is_live"]
        ):
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()
            await hashh.set_stream_status(False)
            logger.debug("Automatic Stream-End (2) detected, hashtags puplished.")


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
    response_temp = await generic_http_request(is_live_url, headers, logger=logger)
    if response_temp is None:
        return
    log_ratelimit(settings["log_level"], response_temp)
    response = response_temp.json()
    check_stream_start_message(settings, response)
    check_stream_start(settings, response)
    check_stream_end(settings, response)


async def new_clips_handler(**settings) -> None:
    """Handling function to find new clips and then post them"""
    if not settings["database_synchronized"]:
        await db.sync_db()
        settings["database_synchronized"] = True
    clips = await fetch_new_clips(settings)
    if clips is None:
        return
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
