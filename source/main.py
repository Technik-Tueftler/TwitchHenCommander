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
    app_started()
    bot = Bot(env.app_settings)
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(bot.start())
    twitch_websocket = loop.create_task(websocket_listener(env.app_settings))

    try:
        loop.run_until_complete(asyncio.gather(bot_task, twitch_websocket))
    except KeyboardInterrupt:
        loop.run_until_complete(asyncio.gather(bot_task, twitch_websocket, return_exceptions=True))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
