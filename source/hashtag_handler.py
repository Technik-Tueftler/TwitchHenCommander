#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
import tweepy

from source.environment_verification import app_settings, tweet_settings
from source.constants import (
    HASHTAG_FILE_PATH,
)

app_data = {"allowed": True, "tweets": []}
lock = asyncio.Lock()


async def tweet_hashtags():
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
        hashtags = " ".join(app_data["tweets"])
        file.write(f"{hashtags}\n")
    auth = tweepy.OAuthHandler(app_settings["consumer_key"], app_settings["consumer_secret"])
    auth.set_access_token(app_settings["access_token"], app_settings["access_token_secret"])
    api = tweepy.API(auth)
    tweet_text = tweet_settings["tweet_start_string"] + hashtags + tweet_settings["tweet_end_string"]
    api.update_status(status=tweet_text)


async def end_add_allowance():
    async with lock:
        app_data["allowed"] = False


async def separate_hash(message) -> set:
    sep_hashtags = [
        element
        for element in message.content.lower().split(" ")
        if element.startswith("#")
        and tweet_settings["hashtag_min_length"]
        <= len(element)
        <= tweet_settings["hashtag_max_length"]
        and not element[1].isdigit()
    ]
    return sep_hashtags


async def register_new_hashtags(new_hashtags) -> None:
    async with lock:
        if app_data["allowed"]:
            merged_hashtags = set(app_data["tweets"]).union(set(new_hashtags))
            app_data["tweets"] = list(merged_hashtags)


def app_started() -> None:
    with open(HASHTAG_FILE_PATH, "a", encoding="utf-8") as file:
        file.write(f"Hashtag-Bot startet: {datetime.utcnow()} UTC \n")


def main() -> None:
    pass


if __name__ == "__main__":
    main()
