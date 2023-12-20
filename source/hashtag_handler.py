#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
All functions to collect the hashtags and send the collected to the configured platforms
"""
import asyncio
from datetime import datetime
from requests import post
import twitchio

import environment_verification as env
from constants import (
    HASHTAG_FILE_PATH,
)

app_data = {"allowed": True, "tweets": []}
lock = asyncio.Lock()


async def delete_hashtags() -> None:
    """
    Delete the hashtags
    :return: None
    """
    app_data["tweets"] = []


async def tweet_hashtags() -> None:
    """
    Send all the hashtags to the configured platforms
    :return: None
    """
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"Hashtags ({datetime.utcnow()} UTC): ")
        hashtags = " ".join(app_data["tweets"])
        file.write(f"{hashtags}\n")
    if env.app_settings["dc_available"]:
        content = (
            env.tweet_settings["tweet_start_string"]
            + hashtags
            + " "
            + env.tweet_settings["tweet_end_string"]
        )
        data = {"content": content, "username": env.app_settings["discord_username"]}
        post(env.app_settings["webhook_url"], data=data, timeout=10)
    app_data["tweets"] = []


async def allow_collecting(allowance: bool) -> None:
    """
    Function to protect the information if app is allowed to collect the hashtags and set the
    status of allowance
    :param allowance: Status of collecting is allowed as bool
    :return: None
    """
    async with lock:
        app_data["allowed"] = allowance


async def separate_hash(message: twitchio.message.Message) -> set:
    """
    Separate all Hashtags from a twitch message
    :param message:
    :return:
    """
    converted_message = message.content
    if env.tweet_settings["hashtag_all_lower_case"]:
        converted_message = message.content.lower()
    return [
        element
        for element in converted_message.split(" ")
        if element.startswith("#")
        and env.tweet_settings["hashtag_min_length"]
        <= len(element)
        <= env.tweet_settings["hashtag_max_length"]
        and not element[1].isdigit()
        and element.count('#') <= 1
    ]


async def register_new_hashtags(new_hashtags: list) -> None:
    """
    Prevents duplications and add all new hashtags to app_data.
    :param new_hashtags: List of hashtags from a message
    :return: None
    """
    async with lock:
        merged_hashtags = set(app_data["tweets"]).union(set(new_hashtags))
        app_data["tweets"] = list(merged_hashtags)


def app_started() -> None:
    """
    Function to do stuff if the app started
    :return:
    """
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"Hashtag-Bot startet: {datetime.utcnow()} UTC \n")


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
