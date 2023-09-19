#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os
from twitchio.ext import commands

client_id = os.getenv("CLIENT_ID")
token = os.getenv("TOKEN")
nickname = os.getenv("NICKNAME")
initial_channels = [os.getenv("INIT_CHANNELS")]

hashtags = set()
lock = asyncio.Lock()
test_list = []


async def check_if_broadcaster(message) -> bool:
    if message.author.is_broadcaster:
        return True
    return False


async def check_if_authorized(message) -> bool:
    if message.author.is_broadcaster:
        return True
    if message.author.is_mod:
        return True
    if message.author.is_vip:
        return True
    return False


async def separate_hash(message) -> set:
    new_hashtags = set(
        element.replace("#", "")
        for element in message.content.lower().split(" ")
        if element.startswith("#") and len(element) >= 3
    )
    return new_hashtags


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=token, prefix="!", initial_channels=initial_channels)

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot
        if message.echo:
            return
        print(message.content)
        if await check_if_authorized(message):
            global hashtags  # pylint: disable=global-statement
            async with lock:
                hashtags |= await separate_hash(message)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello {ctx.author.name}!")

    @commands.command()
    async def finish(self, ctx: commands.Context):
        await ctx.send("Bot wird beendet.")
        await self.close()
        exit(0)


def main() -> None:
    bot = Bot()
    bot.run()
    print("Bot wird beendet")


if __name__ == "__main__":
    main()
