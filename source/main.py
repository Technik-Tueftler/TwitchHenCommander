#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function for starting app and bot
"""
import asyncio
import time
import environment_verification as env
from twitch_bot import Bot
from twitch_api_websocket import websocket_listener
from hashtag_handler import app_started


# async def task2(signal_event):
#     print("Task 2 waiting for Task 1 signal")
#     # Warte auf das Signal von task1, bevor task2 gestartet wird
#     await signal_event.wait()
#     await websocket_listener(env.app_settings)


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
    # signal_event = asyncio.Event()
    bot = Bot(env.app_settings)
    # task1_instance = asyncio.create_task(bot.start())
    # task2_instance = asyncio.create_task(websocket_listener(env.app_settings))
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(bot.start())
    twitch_websocket = loop.create_task(websocket_listener(env.app_settings))

    try:
        # await asyncio.gather(task2_instance)
        # await asyncio.gather(task1_instance, task2_instance)
        # loop.run_until_complete(asyncio.gather(bot_task))
        loop.run_until_complete(asyncio.gather(bot_task, twitch_websocket))
        # loop.run_until_complete(asyncio.gather(task1_instance, task2_instance))
        # await task1_instance
        # await task2_instance
    except KeyboardInterrupt:
        # bot_task.cancel()
        # second_task.cancel()
        loop.run_until_complete(asyncio.gather(bot_task, twitch_websocket, return_exceptions=True))
        # loop.run_until_complete(asyncio.gather(bot_task, second_task, return_exceptions=True))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
