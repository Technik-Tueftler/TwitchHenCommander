#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import environment_verification as env
from source.twitch_bot import Bot

data = {"tweets": []}


async def my_second_task():
    while True:
        print("sec Task")
        await asyncio.sleep(3)


def main():
    if not env.setting_verification(): return
    bot = Bot(env.app_settings, data)
    loop = asyncio.get_event_loop()
    bot_task = loop.create_task(bot.start())

    # second_task = loop.create_task(my_second_task())

    try:
        loop.run_until_complete(asyncio.gather(bot_task))
        # loop.run_until_complete(asyncio.gather(bot_task, second_task))
    except KeyboardInterrupt:
        bot_task.cancel()
        # second_task.cancel()
        loop.run_until_complete(asyncio.gather(bot_task, second_task, return_exceptions=True))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
