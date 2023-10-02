#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions and classes for the twitch bot with all allowed commands
"""
import twitchio
from twitchio.ext import commands
import source.hashtag_handler as hashh


async def check_if_command_authorized(ctx: commands.Context) -> bool:
    """
    Check if user has permission to send commands
    :param ctx: Sent message from user
    :return: Allowance as bool
    """
    return ctx.author.is_broadcaster


async def check_if_hash_authorized(message: twitchio.message.Message) -> bool:
    """
    Check if user has permission to register hashtags
    :param message: Sent message from user
    :return: Allowance as bool
    """
    if message.author.is_broadcaster:
        return True
    return True if message.author.is_mod else bool(message.author.is_vip)


class Bot(commands.Bot):
    """
    Twitch bot to start twitch chat listening and check all messages for hashtags
    and commands.
    """
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
            if await check_if_hash_authorized(message):
                new_hashtags = await hashh.separate_hash(message)
                if len(new_hashtags) > 0:
                    await hashh.register_new_hashtags(new_hashtags)

        await self.handle_commands(message)

    @commands.command()
    async def finishHash(self, ctx: commands.Context):  # pylint: disable=invalid-name
        """
        Function command to finish collecting hashtags and send them
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not check_if_command_authorized:
            return
        if hashh.app_data["allowed"]:
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()
            await ctx.send("Hashtag-Bot is finished and data is sent.")
        # await self.close()
        # exit(0)

    @commands.command()
    async def startHash(self, ctx: commands.Context) -> None:  # pylint: disable=invalid-name
        """
        Function command to start collecting hashtags
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not check_if_command_authorized:
            return
        if not hashh.app_data["allowed"]:
            await hashh.allow_collecting(True)
            await ctx.send("Hashtag-Bot is running.")


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
