"""
File contains all constants for easy central import and usage.
"""
CONFIGURATION_FILE_PATH = "../files/config.json"
HASHTAG_FILE_PATH = "../files/hashtags.txt"
LOG_FILE_PATH = "../files/log.txt"
HASHTAG_MAX_LENGTH = 10
HASHTAG_MIN_LENGTH = 3
TWEET_MAX_LENGTH = 280
TWEET_START_STRING = "Highlights: "
TWEET_END_STRING = "Thanks!"
HASHTAG_ALL_LOWER_CASE = False
TWITCH_WEBSOCKET_URL = "wss://eventsub.wss.twitch.tv/ws"
TWITCH_SUBSCRIPTION_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"
REQUEST_TIMEOUT = 10
START_BOT_AT_STREAMSTART = False
FINISH_BOT_AT_STREAMEND = False
PUBLISH_NEW_CLIPS = False
UPDATE_INTERVAL_PUBLISH_NEW_CLIPS = 30
DC_FEATURE_HASHTAG = "off"
DC_FEATURE_CLIPS = "off"
BOT_COMMAND_PATTERN = r"^[A-Za-z0-9]+$"
BOT_HASHTAG_COMMAND_START = "starthash"
BOT_HASHTAG_COMMAND_FINISH = "finishhash"
BOT_HASHTAG_COMMAND_STOP = "stophash"
BOT_HASHTAG_COMMAND_STATUS = "statushash"
BOT_HASHTAG_COMMAND_HELP = "helphash"
HASHTAG_AUTHENTICATION_LEVEL = "BROADCASTER"
OPTIONS_POSITIVE_ARG = ("true", "on", "1", "t", "active")
