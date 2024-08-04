#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions and classes for the twitch bot with all allowed commands
"""
import twitchio
from twitchio.ext import commands
import hashtag_handler as hashh
import environment_verification as env
from watcher import logger


async def check_if_command_authorized(ctx: commands.Context) -> bool:
    """
    Check if user has permission to send commands
    :param ctx: Sent message from user
    :return: Allowance as bool
    """
    return ctx.author.is_broadcaster


async def check_if_setting_change_authorized(message: twitchio.message.Message) -> bool:
    """
    Check if user has permission to change the hashtag rules
    :param message: Sent message from user
    :return: Allowance as bool
    """
    if message.author.is_broadcaster or message.author.is_mod:
        return True
    return False


async def check_if_hash_authorized(message: twitchio.message.Message) -> bool:
    """
    Check if user has permission to register hashtags
    :param message: Sent message from user
    :return: Allowance as bool
    """
    level = env.AuthenticationLevel.EVERYONE
    if message.author.is_subscriber:
        level = env.AuthenticationLevel.SUBSCRIBER
    if message.author.is_vip:
        level = env.AuthenticationLevel.VIP
    if message.author.is_mod:
        level = env.AuthenticationLevel.MOD
    if message.author.is_broadcaster:
        level = env.AuthenticationLevel.BROADCASTER
    return level.value >= env.tweet_settings["hashtag_authentication_level"].value


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
        logger.info(f"Logged in as {self.nick} with id: {self.user_id}.")

    async def event_message(self, message):
        # Messages with echo set to True are messages sent by the bot
        if message.echo:
            return
        if hashh.app_data["allowed"]:
            if await check_if_hash_authorized(message):
                new_hashtags = await hashh.separate_hash(message)
                if len(new_hashtags) > 0:
                    reviewed_hashtags = await hashh.review_hashtags(
                        new_hashtags, message.author.display_name
                    )
                    if len(reviewed_hashtags) > 0:
                        await hashh.register_new_hashtags(reviewed_hashtags)

        await self.handle_commands(message)


    async def event_command_error(self, context: commands.Context, error: Exception):
        if isinstance(error, commands.CommandNotFound):
            return


    @commands.command(name=env.bot_hashtag_commands["finish_hashtag_bot_command"])
    async def finish_hash(self, ctx: commands.Context):
        """
        Function command to finish collecting hashtags and send them
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not await check_if_command_authorized(ctx):
            return
        if hashh.app_data["allowed"]:
            await hashh.allow_collecting(False)
            await hashh.tweet_hashtags()
            await ctx.send("Hashtag-Bot is finished and data is sent.")

    @commands.command(name=env.bot_hashtag_commands["stop_hashtag_bot_command"])
    async def stop_hash(self, ctx: commands.Context):
        """
        Function command to stop collecting hashtags and delete them
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not await check_if_command_authorized(ctx):
            return
        if hashh.app_data["allowed"]:
            await hashh.allow_collecting(False)
            await hashh.delete_hashtags()
            await ctx.send("Hashtag-Bot is stopped and hashtags are deleted.")

    @commands.command(name=env.bot_hashtag_commands["blacklist_hashtag_bot_command"])
    async def blacklist_hash(self, ctx: commands.Context):
        """Function command to add new banned hashtags to blacklist.

        Args:
            ctx (commands.Context): Context for bot to send a message
        """
        if not await check_if_setting_change_authorized(ctx):
            return
        new_hashtags = await hashh.separate_hash(ctx.message)
        await hashh.add_hashtag_blacklist(new_hashtags)
        await hashh.write_blacklist()
        logger.info(
            f"{ctx.message.author.display_name} has added: {new_hashtags} to banned list."
        )

    @commands.command(name=env.bot_hashtag_commands["start_hashtag_bot_command"])
    async def start_hash(self, ctx: commands.Context) -> None:
        """
        Function command to start collecting hashtags
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not await check_if_command_authorized(ctx):
            return
        if not hashh.app_data["allowed"]:
            await hashh.allow_collecting(True)
            await ctx.send("Hashtag-Bot is running.")


    @commands.command(name=env.bot_hashtag_commands["status_hashtag_bot_command"])
    async def status_hash(self, ctx: commands.Context) -> None:
        """
        Function command to get current status of bot
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not await check_if_command_authorized(ctx):
            return
        if hashh.app_data["allowed"]:
            await ctx.send("Hashtag-Bot is running and ready to collect hashtags.")
        else:
            await ctx.send("Hashtag-Bot is paused and waiting for start-command.")

    @commands.command(name=env.bot_hashtag_commands["help_hashtag_bot_command"])
    async def help_hash(self, ctx: commands.Context) -> None:
        """
        Function command to get all hashtag bot commands
        :param ctx: Context for bot to send a message
        :return: None
        """
        if not await check_if_command_authorized(ctx):
            return
        message = f"!{env.bot_hashtag_commands['status_hashtag_bot_command']} (get status of bot), \
            !{env.bot_hashtag_commands['start_hashtag_bot_command']} (start hashtag collecting), \
            !{env.bot_hashtag_commands['finish_hashtag_bot_command']} \
            (finish hashtag collecting and tweet), \
            !{env.bot_hashtag_commands['stop_hashtag_bot_command']} \
            (stop hashtag collecting and delete hashtags)"
        await ctx.send(message)


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
