#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
from requests import post

import environment_verification as env
from source.constants import (
    HASHTAG_FILE_PATH,
)

app_data = {"allowed": True, "tweets": []}
lock = asyncio.Lock()


async def tweet_hashtags():
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
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
        post(env.app_settings["webhook_url"], data=data)
    app_data["tweets"] = []


async def end_add_allowance():
    async with lock:
        app_data["allowed"] = False


async def start_add_allowance():
    async with lock:
        app_data["allowed"] = True


async def separate_hash(message) -> set:
    sep_hashtags = [
        element
        for element in message.content.lower().split(" ")
        if element.startswith("#")
        and env.tweet_settings["hashtag_min_length"]
        <= len(element)
        <= env.tweet_settings["hashtag_max_length"]
        and not element[1].isdigit()
    ]
    return sep_hashtags


async def register_new_hashtags(new_hashtags) -> None:
    async with lock:
        merged_hashtags = set(app_data["tweets"]).union(set(new_hashtags))
        app_data["tweets"] = list(merged_hashtags)


def app_started() -> None:
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"Hashtag-Bot startet: {datetime.utcnow()} UTC \n")


def main() -> None:
    pass


if __name__ == "__main__":
    main()
