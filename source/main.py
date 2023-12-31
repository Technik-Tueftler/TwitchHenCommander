#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main function for starting app and bot
"""
import asyncio
import environment_verification as env
from twitch_bot import Bot
from hashtag_handler import app_started


# async def my_second_task():
#     while True:
#         print("sec Task")
#         await asyncio.sleep(3)


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
    # clip_task = loop.create_task(my_second_task())

    try:
        loop.run_until_complete(asyncio.gather(bot_task))
        # loop.run_until_complete(asyncio.gather(bot_task, second_task))
    except KeyboardInterrupt:
        bot_task.cancel()
        # second_task.cancel()
        loop.run_until_complete(asyncio.gather(bot_task, return_exceptions=True))
        # loop.run_until_complete(asyncio.gather(bot_task, second_task, return_exceptions=True))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
