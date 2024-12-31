#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function for starting app and bot
"""
import asyncio
import environment_verification as env
from constants import APP_VERSION
from twitch_bot import Bot
from twitch_api import new_clips_handler, streaming_handler
from youtube_api import new_yt_video_handler
from watcher import logger
import hashtag_handler as hashh


async def every(__seconds: float, func, *args, **kwargs):
    """Function to call cyclic another function

    Args:
        __seconds (float): Time at which the function is to be called
        func (_type_): Function to be called
    """
    while True:
        await func(*args, **kwargs)
        await asyncio.sleep(__seconds)


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """
    if not env.twitch_setting_verification():
        return
    env.check_tweet_settings()
    env.discord_setting_verification()
    env.bot_setting_verification()
    env.clip_collection_setting_verification()
    env.youtube_setting_verification()
    env.log_settings()
    hashh.init_blacklist()
    bot = Bot(env.app_settings)
    loop = asyncio.get_event_loop()
    tasks_to_start = []
    bot_task = loop.create_task(bot.start())
    tasks_to_start.append(bot_task)
    logger.info(f"App started in version: {APP_VERSION}")
    if any(
        [
            env.app_settings["start_bot_at_streamstart"],
            env.app_settings["finish_bot_at_streamend"],
            env.app_settings["dc_feature_message_streamstart"],
        ]
    ):
        stream_handler = loop.create_task(
            every(
                env.app_settings["check_stream_interval"],
                streaming_handler,
                **env.app_settings
            )
        )
        tasks_to_start.append(stream_handler)
    if env.app_settings["dc_feature_clips"]:
        new_clips = loop.create_task(
            every(
                env.app_settings["clips_fetch_time"],
                new_clips_handler,
                **env.app_settings,
                **env.discord_settings
            )
        )
        tasks_to_start.append(new_clips)
    if env.app_settings["yt_feature_new_video"]:
        new_yt_videos = loop.create_task(
            every(
                env.app_settings["yt_new_video_fetch_time"],
                new_yt_video_handler,
                **env.app_settings,
                **env.youtube_settings,
                **env.discord_settings
            )
        )
        tasks_to_start.append(new_yt_videos)
    loop.run_until_complete(asyncio.gather(*tasks_to_start))


if __name__ == "__main__":
    main()
