#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function for starting app and bot
"""
import asyncio
import environment_verification as env
from twitch_bot import Bot
from twitch_api_websocket import websocket_listener
from hashtag_handler import app_started


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
    app_started()
    bot = Bot(env.app_settings)
    loop = asyncio.get_event_loop()
    tasks_to_start = []
    bot_task = loop.create_task(bot.start())
    tasks_to_start.append(bot_task)
    if any(
        [
            env.app_settings["start_bot_at_streamstart"],
            env.app_settings["finish_bot_at_streamend"],
        ]
    ):
        twitch_websocket = loop.create_task(websocket_listener(env.app_settings))
        tasks_to_start.append(twitch_websocket)
    loop.run_until_complete(asyncio.gather(*tasks_to_start))


if __name__ == "__main__":
    main()
