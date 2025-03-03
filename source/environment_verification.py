#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Checks if all environment variables and input are given and provides helper functions.
"""
import os
import re
from enum import Enum
import requests
from dotenv import dotenv_values
from watcher import logger, init_logging

from constants import (
    HASHTAG_MAX_LENGTH,
    HASHTAG_MIN_LENGTH,
    TWEET_MAX_LENGTH,
    HASHTAG_ALL_LOWER_CASE,
    REQUEST_TIMEOUT,
    BOT_HASHTAG_COMMAND_START,
    BOT_HASHTAG_COMMAND_FINISH,
    BOT_HASHTAG_COMMAND_STOP,
    BOT_HASHTAG_COMMAND_HELP,
    BOT_HASHTAG_COMMAND_STATUS,
    BOT_HASHTAG_COMMAND_BANN,
    HASHTAG_AUTHENTICATION_LEVEL,
    DC_FEATURE_HASHTAG,
    DC_FEATURE_CLIPS,
    OPTIONS_POSITIVE_ARG,
    BOT_COMMAND_PATTERN,
    CLIP_THANK_YOU_TEXT,
    UPDATE_INTERVAL_PUBLISH_NEW_CLIPS,
    CHECK_STREAM_INTERVAL,
    LOG_LEVEL,
    OPTIONS_LOG_LEVEL,
    DC_FEATURE_MESSAGE_STREAMSTART,
    DC_FEATURE_MESSAGE_STREAMSTART_TEXT,
    HASHTAG_CHATTER_THANKS_TEXT,
    HASHTAG_FEATURE_FROM_STREAM_TAGS,
    STREAM_START_TIME_DIFFERENCE,
    START_BOT_AT_STREAMSTART,
    FINISH_BOT_AT_STREAMEND,
    YT_VIDEO_FETCH_TIME,
    YT_POST_TEXT,
    DC_FEATURE_LINKS,
    YT_API_MAX_REQUESTS_S,
    APP_VERSION,
    DC_MESSAGE_STREAMSTART_NOTI_ROLE_NO_PATTERN,
    DC_MESSAGE_STREAMSTART_NOTI_ROLE_REPLACEMENT,
)


config = {
    **dotenv_values("../files/.env"),
    **os.environ,
}


class AuthenticationLevel(Enum):
    """Privileges for chatters to limit the use of features"""

    BROADCASTER = 4
    MOD = 3
    VIP = 2
    SUBSCRIBER = 1
    EVERYONE = 0


client_id = config.get("TW_CLIENT_ID", None)
token = config.get("TW_TOKEN", None)
nickname = config.get("TW_NICKNAME", None)
init_channels = config.get("TW_INIT_CHANNELS", None)
broadcaster_id = config.get("TW_BROADCASTER_ID", None)
check_stream_interval = config.get("CHECK_STREAM_INTERVAL", CHECK_STREAM_INTERVAL)
log_level_env = config.get("LOG_LEVEL", LOG_LEVEL)
discord_username_hashtag = config.get("DC_USER_NAME_HASHTAG", None)
webhook_url_hashtag = config.get("DC_WEBHOOK_URL_HASHTAG", None)
discord_username_clip = config.get("DC_USER_NAME_CLIP", None)
webhook_url_clip = config.get("DC_WEBHOOK_URL_CLIP", None)
dc_feature_hashtag = config.get("DC_FEATURE_HASHTAG", DC_FEATURE_HASHTAG)
dc_feature_clips = config.get("DC_FEATURE_CLIPS", DC_FEATURE_CLIPS)
discord_username_links = config.get(
    "",
)
webhook_url_links = config.get(
    "",
)
dc_feature_links = config.get("DC_FEATURE_LINKS", DC_FEATURE_LINKS)
clip_thank_you_text = config.get("CLIP_THANK_YOU_TEXT", CLIP_THANK_YOU_TEXT)
clips_fetch_time = config.get("CLIPS_FETCH_TIME", UPDATE_INTERVAL_PUBLISH_NEW_CLIPS)
dc_feature_message_streamstart = config.get(
    "DC_FEATURE_MESSAGE_STREAMSTART", DC_FEATURE_MESSAGE_STREAMSTART
)
dc_feature_message_streamstart_time_diff = config.get(
    "STREAM_START_TIME_DIFFERENCE", STREAM_START_TIME_DIFFERENCE
)
dc_username_message_streamstart = config.get("DC_USER_NAME_MESSAGE_STREAMSTART", None)
webhook_url_message_streamstart = config.get("DC_WEBHOOK_URL_MESSAGE_STREAMSTART", None)
dc_feature_message_streamstart = config.get(
    "DC_FEATURE_MESSAGE_STREAMSTART", DC_FEATURE_MESSAGE_STREAMSTART
)
dc_feature_message_streamstart_text = config.get(
    "DC_FEATURE_MESSAGE_STREAMSTART_TEXT", DC_FEATURE_MESSAGE_STREAMSTART_TEXT
)
hashtag_max_length = config.get("HASHTAG_MAX_LENGTH", HASHTAG_MAX_LENGTH)
hashtag_min_length = config.get("HASHTAG_MIN_LENGTH", HASHTAG_MIN_LENGTH)
tweet_max_length = config.get("TWEET_MAX_LENGTH", TWEET_MAX_LENGTH)
hashtag_all_lower_case = config.get("HASHTAG_ALL_LOWER_CASE", HASHTAG_ALL_LOWER_CASE)
hashtag_authentication_level = config.get(
    "HASHTAG_AUTHENTICATION_LEVEL", HASHTAG_AUTHENTICATION_LEVEL
)
hashtag_chatter_thanks_text = config.get(
    "HASHTAG_CHATTER_THANKS_TEXT", HASHTAG_CHATTER_THANKS_TEXT
)
hashtag_from_stream_tags = config.get(
    "HASHTAG_FEATURE_FROM_STREAM_TAGS", HASHTAG_FEATURE_FROM_STREAM_TAGS
)
start_bot_at_streamstart = config.get(
    "START_BOT_AT_STREAMSTART", START_BOT_AT_STREAMSTART
)
finish_bot_at_streamend = config.get("FINISH_BOT_AT_STREAMEND", FINISH_BOT_AT_STREAMEND)
start_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_START", BOT_HASHTAG_COMMAND_START
)
finish_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_FINISH", BOT_HASHTAG_COMMAND_FINISH
)
stop_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_STOP", BOT_HASHTAG_COMMAND_STOP
)
help_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_HELP", BOT_HASHTAG_COMMAND_HELP
)
status_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_STATUS", BOT_HASHTAG_COMMAND_STATUS
)
blacklist_hashtag_bot_command = config.get(
    "BOT_HASHTAG_COMMAND_BANN", BOT_HASHTAG_COMMAND_BANN
)
youtube_token = config.get("YT_TOKEN", None)
youtube_channel_id = config.get("YT_CHANNEL_ID", None)
yt_new_video_fetch_time = config.get("YT_VIDEO_FETCH_TIME", YT_VIDEO_FETCH_TIME)
discord_username_video = config.get("DC_USER_NAME_YT", None)
webhook_url_video = config.get("DC_WEBHOOK_URL_YT", None)
yt_post_text = config.get("YT_POST_TEXT", YT_POST_TEXT)

bot_command_pattern = re.compile(BOT_COMMAND_PATTERN)
dc_noti_role_pattern = re.compile(DC_MESSAGE_STREAMSTART_NOTI_ROLE_NO_PATTERN)

app_settings = {
    "ID": client_id,
    "token": token,
    "nickname": nickname,
    "broadcaster_id": broadcaster_id,
    "channels": None,
    "dc_available": False,
    "dc_feature_hashtag": False,
    "dc_feature_clips": False,
    "dc_feature_links": False,
    "dc_feature_start_message": False,
    "check_stream_interval": CHECK_STREAM_INTERVAL,
    "clips_fetch_time": clips_fetch_time,
    "database_synchronized": False,
    "start_bot_at_streamstart": start_bot_at_streamstart,
    "finish_bot_at_streamend": finish_bot_at_streamend,
    "log_level": log_level_env,
    "yt_feature_new_video": False,
    "yt_new_video_fetch_time": yt_new_video_fetch_time,
}

bot_hashtag_commands = {
    "start_hashtag_bot_command": start_hashtag_bot_command,
    "finish_hashtag_bot_command": finish_hashtag_bot_command,
    "stop_hashtag_bot_command": stop_hashtag_bot_command,
    "help_hashtag_bot_command": help_hashtag_bot_command,
    "status_hashtag_bot_command": status_hashtag_bot_command,
    "blacklist_hashtag_bot_command": blacklist_hashtag_bot_command,
}

tweet_settings = {
    "hashtag_max_length": HASHTAG_MAX_LENGTH,
    "hashtag_min_length": HASHTAG_MIN_LENGTH,
    "hashtag_all_lower_case": HASHTAG_ALL_LOWER_CASE,
    "hashtag_authentication_level": AuthenticationLevel[HASHTAG_AUTHENTICATION_LEVEL],
    "hashtag_pattern": None,
    "hashtag_chatter_thanks_text": HASHTAG_CHATTER_THANKS_TEXT,
    "hashtag_from_stream_tags": HASHTAG_FEATURE_FROM_STREAM_TAGS,
}

discord_settings = {
    "discord_username_hashtag": discord_username_hashtag,
    "webhook_url_hashtag": webhook_url_hashtag,
    "discord_username_clip": discord_username_clip,
    "webhook_url_clip": webhook_url_clip,
    "clip_thank_you_text": clip_thank_you_text,
    "dc_username_message_streamstart": dc_username_message_streamstart,
    "webhook_url_message_streamstart": webhook_url_message_streamstart,
    "dc_feature_message_streamstart_text": dc_feature_message_streamstart_text,
    "dc_feature_message_streamstart_time_diff": dc_feature_message_streamstart_time_diff,
    "discord_username_video": discord_username_video,
    "webhook_url_video": webhook_url_video,
    "discord_username_links": discord_username_links,
    "webhook_url_links": webhook_url_links,
    "dc_message_streamstart_noti_role": None
}

youtube_settings = {
    "youtube_token": youtube_token,
    "youtube_channel_id": youtube_channel_id,
    "yt_post_text": yt_post_text,
}


def log_settings() -> None:
    """Log all settings for user information"""
    log_level = app_settings["log_level"]
    streamstart = app_settings["start_bot_at_streamstart"]
    streamend = app_settings["finish_bot_at_streamend"]
    dc_hashtags = app_settings["dc_feature_hashtag"]
    dc_clips = app_settings["dc_feature_clips"]
    dc_yt = app_settings["yt_feature_new_video"]
    clips_fetch_time_setting = app_settings["clips_fetch_time"]
    yt_fetch_time_setting = app_settings["yt_new_video_fetch_time"]
    online_check_time = app_settings["check_stream_interval"]
    logger.info("=" * 25)
    logger.info(" Settings")
    logger.info("=" * 25)
    logger.info("*" * 25)
    logger.info(" Hen Commander")
    logger.info("*" * 25)
    logger.info(f"Version:   {APP_VERSION}")
    logger.info(f"Log-Level: {log_level}")
    logger.info("*" * 25)
    logger.info("*" * 25)
    logger.info(" Hashtag-Feature")
    logger.info("*" * 25)
    logger.info(f"#-Collection active: {dc_hashtags}")
    logger.info(f"Automatik Start:     {streamstart}")
    logger.info(f"Automatik End:       {streamend}")
    logger.debug(f"Onlinestatus time (loaded from env): {check_stream_interval}")
    logger.info(f"Onlinestatus time: {online_check_time}")
    logger.info("*" * 25)
    logger.info("*" * 25)
    logger.info(" Clip-Feature")
    logger.info("*" * 25)
    logger.info(f"Clip-Fetch active: {dc_clips}")
    logger.debug(f"Clip-Fetch time (loaded from env): {clips_fetch_time}")
    logger.info(f"Clip-Fetch time: {clips_fetch_time_setting}")
    logger.info("*" * 25)
    logger.info("*" * 25)
    logger.info(" Video-Feature")
    logger.info(f"Video-Fetch active: {dc_yt}")
    logger.debug(f"Video-Fetch time (loaded from env): {yt_new_video_fetch_time}")
    logger.info(f"Video-Fetch time: {yt_fetch_time_setting}")
    logger.info("*" * 25)
    logger.info("*" * 25)
    logger.debug(" Loaded text environment variables")
    logger.debug(f"Thank you text: {hashtag_chatter_thanks_text}")
    logger.debug(f"Stream start message: {dc_feature_message_streamstart_text}")
    logger.debug(f"Youtube post text: {yt_post_text}")
    logger.info("=" * 25)


def bot_setting_verification() -> None:
    """
    Check if bot settings are available or app have to use the generic ones
    :return: None
    """
    bot_hashtag_commands["start_hashtag_bot_command"] = (
        start_hashtag_bot_command
        if re.match(bot_command_pattern, start_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_START
    )
    bot_hashtag_commands["finish_hashtag_bot_command"] = (
        finish_hashtag_bot_command
        if re.match(bot_command_pattern, finish_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_FINISH
    )
    bot_hashtag_commands["stop_hashtag_bot_command"] = (
        stop_hashtag_bot_command
        if re.match(bot_command_pattern, stop_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_STOP
    )
    bot_hashtag_commands["help_hashtag_bot_command"] = (
        help_hashtag_bot_command
        if re.match(bot_command_pattern, help_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_HELP
    )
    bot_hashtag_commands["status_hashtag_bot_command"] = (
        status_hashtag_bot_command
        if re.match(bot_command_pattern, status_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_STATUS
    )
    bot_hashtag_commands["blacklist_hashtag_bot_command"] = (
        blacklist_hashtag_bot_command
        if re.match(bot_command_pattern, blacklist_hashtag_bot_command)
        else BOT_HASHTAG_COMMAND_BANN
    )
    app_settings["start_bot_at_streamstart"] = start_bot_at_streamstart.lower() in (
        OPTIONS_POSITIVE_ARG
    )
    app_settings["finish_bot_at_streamend"] = finish_bot_at_streamend.lower() in (
        OPTIONS_POSITIVE_ARG
    )
    app_settings["dc_feature_message_streamstart"] = (
        dc_feature_message_streamstart.lower() in (OPTIONS_POSITIVE_ARG)
    )


def check_tweet_settings():
    """
    Check if config file available and the tweet settings and write the result in the tweet settings
    :return: None
    """
    tweet_settings["hashtag_max_length"] = (
        int(hashtag_max_length)
        if hashtag_max_length.isdecimal()
        else int(HASHTAG_MAX_LENGTH)
    )
    tweet_settings["hashtag_min_length"] = (
        int(hashtag_min_length)
        if hashtag_min_length.isdecimal()
        else int(HASHTAG_MIN_LENGTH)
    )
    tweet_settings["tweet_max_length"] = (
        int(tweet_max_length) if tweet_max_length.isdecimal() else int(TWEET_MAX_LENGTH)
    )
    tweet_settings["hashtag_all_lower_case"] = hashtag_all_lower_case.lower() in (
        OPTIONS_POSITIVE_ARG
    )
    tweet_settings["hashtag_from_stream_tags"] = hashtag_from_stream_tags.lower() in (
        OPTIONS_POSITIVE_ARG
    )
    tweet_settings["hashtag_authentication_level"] = (
        AuthenticationLevel[hashtag_authentication_level]
        if hashtag_authentication_level.upper() in AuthenticationLevel.__members__
        else AuthenticationLevel[HASHTAG_AUTHENTICATION_LEVEL]
    )
    tweet_settings["hashtag_pattern"] = re.compile(
        r"\B#(?![0-9_]+)\w{"
        + str(tweet_settings["hashtag_min_length"])
        + r","
        + str(tweet_settings["hashtag_max_length"])
        + r"}\b"
    )


def check_twitch_env_available() -> bool:
    """
    Check if environment variables available for twitch settings
    :return: result if settings available as bool
    """
    if log_level_env.upper() in OPTIONS_LOG_LEVEL:
        app_settings["log_level"] = log_level_env.upper()
    else:
        app_settings["log_level"] = LOG_LEVEL
    init_logging(app_settings["log_level"])

    if check_stream_interval.isdecimal():
        app_settings["check_stream_interval"] = int(check_stream_interval)
    else:
        app_settings["check_stream_interval"] = int(CHECK_STREAM_INTERVAL)
        logger.info(
            f"Value for CHECK_STREAM_INTERVAL is not an integer and has been set to "
            f"default value: {CHECK_STREAM_INTERVAL}"
        )
    return None not in (client_id, token, nickname, init_channels)


def twitch_setting_verification() -> bool:
    """
    Check if all twitch information are available and write the result in the app settings
    :return: None
    """
    if check_twitch_env_available():
        app_settings["channels"] = init_channels.split(",")
        url = f"https://api.twitch.tv/helix/users?login={app_settings['nickname']}"
        headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT).json()
        app_settings["broadcaster_id"] = response["data"][0]["id"]
        return True
    logger.error("The login data for twitch is missing or incomplete.")
    return False


def discord_setting_verification() -> None:
    """
    Check if all discord information are available and write the result in the app settings
    :return: None
    """
    if dc_feature_hashtag.lower() in (OPTIONS_POSITIVE_ARG):
        if None not in (
            discord_settings["discord_username_hashtag"],
            discord_settings["webhook_url_hashtag"],
        ):
            app_settings["dc_feature_hashtag"] = True
    if dc_feature_clips is not None and dc_feature_clips.lower() in (
        OPTIONS_POSITIVE_ARG
    ):
        if None not in (
            discord_settings["discord_username_clip"],
            discord_settings["webhook_url_clip"],
        ):
            app_settings["dc_feature_clips"] = True
    if (
        dc_feature_message_streamstart is not None
        and dc_feature_message_streamstart.lower() in (OPTIONS_POSITIVE_ARG)
    ):
        if None not in (
            discord_settings["dc_username_message_streamstart"],
            discord_settings["webhook_url_message_streamstart"],
        ):
            app_settings["dc_feature_start_message"] = True
    if any(
        [
            app_settings["dc_feature_clips"],
            app_settings["dc_feature_hashtag"],
            app_settings["dc_feature_start_message"],
        ]
    ):
        app_settings["dc_available"] = True
    app_settings["clips_fetch_time"] = (
        int(clips_fetch_time)
        if clips_fetch_time.isdecimal()
        else int(UPDATE_INTERVAL_PUBLISH_NEW_CLIPS)
    )
    discord_settings["dc_feature_message_streamstart_time_diff"] = (
        int(dc_feature_message_streamstart_time_diff)
        if dc_feature_message_streamstart_time_diff.isdecimal()
        else int(STREAM_START_TIME_DIFFERENCE)
    )
    if dc_feature_links is not None and dc_feature_links.lower() in (
        OPTIONS_POSITIVE_ARG
    ):
        if None not in (
            discord_settings["discord_username_links"],
            discord_settings["webhook_url_links"],
        ):
            app_settings["dc_feature_links"] = True
    logger.extdebug(f"Loaded streamstart text: {dc_feature_message_streamstart_text}")
    match_noti_role = re.search(
        DC_MESSAGE_STREAMSTART_NOTI_ROLE_NO_PATTERN, dc_feature_message_streamstart_text
    )
    if match_noti_role:
        discord_settings["dc_message_streamstart_noti_role"] = (
            f"<@&{match_noti_role.group(1)}>"
        )
        logger.extdebug(f"Found role: {discord_settings['dc_message_streamstart_noti_role']}")
        logger.extdebug(f"Founded group 0: {match_noti_role.group(0)}")
        logger.extdebug(f"Input stream text : {dc_feature_message_streamstart_text}")
        replacement_string = re.sub(
            match_noti_role.group(0),
            DC_MESSAGE_STREAMSTART_NOTI_ROLE_REPLACEMENT,
            dc_feature_message_streamstart_text,
        )
        logger.extdebug(f"Replacement string: {replacement_string}")
        discord_settings["dc_feature_message_streamstart_text"] = replacement_string

def clip_collection_setting_verification() -> None:
    """
    Check if settings are available for collecting new clips
    :return: None
    """
    app_settings["dc_feature_clips"] = dc_feature_clips.lower() in (
        OPTIONS_POSITIVE_ARG
    )


def youtube_setting_verification() -> None:
    """
    Check if settings are available for youtube configurations
    """
    app_settings["yt_feature_new_video"] = None not in (
        youtube_token,
        youtube_channel_id,
    )
    if (
        not yt_new_video_fetch_time.isdecimal()
        or int(yt_new_video_fetch_time) < YT_API_MAX_REQUESTS_S
    ):
        app_settings["yt_new_video_fetch_time"] = int(YT_VIDEO_FETCH_TIME)
        logger.info(
            f"Youtube fetch time <{yt_new_video_fetch_time}> is not decimal or smaller "
            f"than the allowed request time <{YT_API_MAX_REQUESTS_S}>. "
            f"The time is set to the default value of {YT_VIDEO_FETCH_TIME}."
        )
        app_settings["yt_new_video_fetch_time"] = YT_API_MAX_REQUESTS_S
        return
    app_settings["yt_new_video_fetch_time"] = int(yt_new_video_fetch_time)


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """
    twitch_setting_verification()


if __name__ == "__main__":
    main()
