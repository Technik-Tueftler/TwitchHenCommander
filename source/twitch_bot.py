#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import asyncio
import os
from twitchio.ext import commands

lock = asyncio.Lock()


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
    sep_hashtags = [element.replace("#", "")
                    for element in message.content.lower().split(" ")
                    if element.startswith("#") and 3 <= len(element) <= 10
                    ]
    return sep_hashtags


async def register_new_hashtags(data: dict, new_hashtags) -> None:
    async with lock:
        merged_hashtags = set(data["tweets"]).union(set(new_hashtags))
        data["tweets"] = list(merged_hashtags)


class Bot(commands.Bot):
    def __init__(self, settings: list, data: dict):
        super().__init__(token=settings["token"], prefix="!", initial_channels=settings["channels"])
        self.settings = settings
        self.data = data

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot
        if message.echo:
            return
        print(message.content)
        if await check_if_authorized(message):
            new_hashtags = await separate_hash(message)
            await register_new_hashtags(self.data, new_hashtags)

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
    bot = Bot([], {})
    bot.run()
    print("Bot wird beendet")


if __name__ == "__main__":
    main()
