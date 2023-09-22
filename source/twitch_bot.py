#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from twitchio.ext import commands
from source.hashtag_handler import app_data, register_new_hashtags, separate_hash, end_add_allowance,tweet_hashtags


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


class Bot(commands.Bot):
    def __init__(self, settings: list):
        super().__init__(
            token=settings["token"], prefix="!", initial_channels=settings["channels"]
        )
        self.settings = settings

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
            if len(new_hashtags) > 0:
                await register_new_hashtags(new_hashtags)

        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f"Hello {ctx.author.name}!")
        print(app_data)

    @commands.command()
    async def finish(self, ctx: commands.Context):
        await end_add_allowance()
        await tweet_hashtags()
        await ctx.send("Bot wird beendet.")
        await self.close()
        exit(0)


def main() -> None:
    bot = Bot([], {})
    bot.run()
    print("Bot wird beendet")


if __name__ == "__main__":
    main()
