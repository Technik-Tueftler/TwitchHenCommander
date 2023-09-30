#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from twitchio.ext import commands
import source.hashtag_handler as hashh


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
        if hashh.app_data["allowed"]:
            if await check_if_authorized(message):
                new_hashtags = await hashh.separate_hash(message)
                if len(new_hashtags) > 0:
                    await hashh.register_new_hashtags(new_hashtags)

        await self.handle_commands(message)


    @commands.command()
    async def finishHash(self, ctx: commands.Context):
        if hashh.app_data["allowed"]:
            await hashh.end_add_allowance()
            await hashh.tweet_hashtags()
            await ctx.send("Hashtag-Bot is finished and data is sent.")
        #await self.close()
        #exit(0)

    @commands.command()
    async def startHash(self, ctx: commands.Context):
        if not hashh.app_data["allowed"]:
            await hashh.start_add_allowance()
            await ctx.send("Hashtag-Bot is running.")


def main() -> None:
    bot = Bot([], {})
    bot.run()
    print("Bot wird beendet")


if __name__ == "__main__":
    main()
