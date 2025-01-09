#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All functions to collect the hashtags and send the collected to the configured platforms
"""
from pathlib import Path
import asyncio
from datetime import datetime, UTC
import aiofiles
from requests import post
import twitchio
from generic_functions import MyTemplate
import environment_verification as env
import db
from watcher import logger
from constants import (
    REQUEST_TIMEOUT,
    HASHTAG_BLACKLIST_FILE_PATH,
    TWITCH_URL,
)

app_data = {
    "online": False,
    "stream_id": None,
    "allowed": True,
    "tweets": [],
    "blacklist": set(),
    "start_message_done": False,
    "chatter": set(),
    "links": set()
}
lock = asyncio.Lock()


async def delete_hashtags() -> None:
    """
    Delete the hashtags
    :return: None
    """
    async with lock:
        app_data["tweets"] = []


async def stream_start_message(response: dict) -> None:
    """Send a Stream-Start information in DC"""
    try:
        broadcaster = response["data"][0]["display_name"]
        genre = response["data"][0]["game_name"]
        link = TWITCH_URL + "/" + broadcaster
        content = MyTemplate(
            env.discord_settings["dc_feature_message_streamstart_text"]
        ).substitute(broadcaster=broadcaster, genre=genre, link=link)
        data = {
            "content": content,
            "username": env.discord_settings["dc_username_message_streamstart"],
        }
        post(
            env.discord_settings["webhook_url_message_streamstart"],
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
        logger.info(f"Send stream-start message: {content}")
    except (KeyError, IndexError) as err:
        logger.error(
            f"The twitch response doesn't have the required key. Message: {err}"
        )


async def tweet_hashtags() -> None:
    """
    Send all the hashtags to the configured platforms
    :return: None
    """
    reviewed_hashtags = await review_hashtags(app_data["tweets"])
    chatter = ", ".join(app_data["chatter"])
    stream_data = {
        "timestamp_end": datetime.now(UTC),
        "hashtags": " ".join(reviewed_hashtags),
        "chatter": chatter,
    }
    stream_id = app_data["stream_id"]
    await db.update_stream(stream_id, stream_data)
    logger.debug(f"Stream data is updated in DB with ID: {stream_id}")

    if len(reviewed_hashtags) <= 0:
        return
    if len(app_data["chatter"]) <= 0:
        app_data["chatter"].add("all")
    content = MyTemplate(env.tweet_settings["hashtag_chatter_thanks_text"]).substitute(
        hashtags=", ".join(reviewed_hashtags),
        chatter=chatter,
    )
    if env.app_settings["dc_available"]:
        data = {
            "content": content,
            "username": env.discord_settings["discord_username_hashtag"],
        }
        post(
            env.discord_settings["webhook_url_hashtag"],
            data=data,
            timeout=REQUEST_TIMEOUT,
        )
    app_data["tweets"] = []
    app_data["chatter"].clear()
    logger.debug(f'Clear chatter and hashtags lists: {app_data["tweets"]} / {app_data["chatter"]}')


async def allow_collecting(allowance: bool) -> None:
    """
    Function to protect the information if app is allowed to collect the hashtags and set the
    status of allowance
    :param allowance: Status of collecting is allowed as bool
    :return: None
    """
    async with lock:
        app_data["allowed"] = allowance


async def set_stream_status(status: bool) -> None:
    """
    Function to protect the information if stream is online or offline and set status
    :param status: Status of stream
    :return: None
    """
    async with lock:
        app_data["online"] = status


async def add_hashtag_blacklist(new_hashtags: set) -> None:
    """Function to protect the information for banned hashtags during blacklist update command

    Args:
        new_hashtags (set): banned hashtags
    """
    async with lock:
        app_data["blacklist"].update(hashtag.lower() for hashtag in new_hashtags)
        logger.info(f"Add hashtags to blacklist: {new_hashtags}")


async def separate_hash(message: twitchio.message.Message) -> set:
    """
    Separate all Hashtags from a twitch message
    :param message:
    :return:
    """
    converted_message = message.content
    if env.tweet_settings["hashtag_all_lower_case"]:
        converted_message = message.content.lower()
    return env.tweet_settings["hashtag_pattern"].findall(converted_message)


async def register_new_hashtags(display_name: str | None, new_hashtags: set) -> None:
    """
    Prevents duplications and add all new hashtags to app_data.
    :display_name: Displayname of chatter
    :param new_hashtags: List of hashtags from a message
    :return: None
    """
    async with lock:
        merged_hashtags = set(app_data["tweets"]).union(set(new_hashtags))
        app_data["tweets"] = list(merged_hashtags)
        if display_name is not None:
            app_data["chatter"].add(display_name)
            logger.info(f"Registered new hashtags: {new_hashtags} from {display_name}")
        else:
            logger.info(f"Registered new hashtags from stream tags: {new_hashtags}")


async def review_hashtags(hashtags: set, author: str = None) -> set:
    """Review the seperated hashtags and check if there are allowed

    Args:
        hashtags (set): new hashtags from message

    Returns:
        set: reviewed hashtags
    """

    def check(hashtag: str):
        if hashtag.lower() not in app_data["blacklist"]:
            return True
        if author is not None:
            logger.info(f"{author} has used hashtag {hashtag}, which is not allowed.")
        return False

    return set(filter(check, hashtags))


def init_blacklist() -> None:
    """Read and init the blacklist for hashtags"""
    if not Path(HASHTAG_BLACKLIST_FILE_PATH).is_file():
        return
    with open(HASHTAG_BLACKLIST_FILE_PATH, "r", encoding="utf-8") as file:
        app_data["blacklist"] = set(
            hashtag.strip().lower()
            for hashtag in file.read().splitlines()
            if hashtag.strip()
        )


async def write_blacklist() -> None:
    """Write new banned hashtags in file"""
    async with aiofiles.open(
        HASHTAG_BLACKLIST_FILE_PATH, mode="w", encoding="utf-8"
    ) as file:
        for string in app_data["blacklist"]:
            await file.write(string + "\n")


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """
    init_blacklist()


if __name__ == "__main__":
    main()
