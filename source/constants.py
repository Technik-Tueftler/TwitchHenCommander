"""
File contains all constants for easy central import and usage.
"""

APP_VERSION = "v1.8.3"
CONFIGURATION_FILE_PATH = "../files/config.json"
CACHE_FILE_PATH = "../files/cache.json"
LOG_FILE_PATH = "../files/log.txt"
HASHTAG_BLACKLIST_FILE_PATH = "../files/blacklist.txt"
HASHTAG_MAX_LENGTH = "10"
HASHTAG_MIN_LENGTH = "3"
TWEET_MAX_LENGTH = "280"
HASHTAG_CHATTER_THANKS_TEXT = (
    "Highlights from stream: #hashtags"
    + ", thanks to #chatter for creating the highlights!"
)
HASHTAG_ALL_LOWER_CASE = False
TWITCH_WEBSOCKET_URL = "wss://eventsub.wss.twitch.tv/ws"
TWITCH_SUBSCRIPTION_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"
TWITCH_URL = "https://www.twitch.tv"
REQUEST_TIMEOUT = 10
START_BOT_AT_STREAMSTART = False
FINISH_BOT_AT_STREAMEND = False
PUBLISH_NEW_CLIPS = False
UPDATE_INTERVAL_PUBLISH_NEW_CLIPS = "30"
DC_FEATURE_HASHTAG = "off"
DC_FEATURE_CLIPS = "off"
DC_FEATURE_LINKS = "off"
BOT_LINK_PATTERN = r"(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
BOT_COMMAND_PATTERN = r"^[A-Za-z0-9]+$"
BOT_HASHTAG_COMMAND_START = "starthash"
BOT_HASHTAG_COMMAND_FINISH = "finishhash"
BOT_HASHTAG_COMMAND_STOP = "stophash"
BOT_HASHTAG_COMMAND_STATUS = "statushash"
BOT_HASHTAG_COMMAND_HELP = "helphash"
BOT_HASHTAG_COMMAND_BANN = "hashblacklist"
DC_FEATURE_MESSAGE_STREAMSTART = "off"
HASHTAG_FEATURE_FROM_STREAM_TAGS = "off"
DC_FEATURE_MESSAGE_STREAMSTART_TEXT = (
    "#broadcaster with #genre is online. It's amazing what's happen here: #link"
)
# (hours * minutes * seconds) / (max yt api requests per day)
YT_API_MAX_REQUESTS_S = (24*60*60)/(100)
YT_VIDEO_FETCH_TIME = "1200"
YT_POST_TEXT = (
    "A new video has been published on #portal. "
    "It's a great video. Take a look right now: #link "
    "and don't forget to comment."
)
# BROADCASTER, MOD, VIP, SUBSCRIBER, EVERYONE
HASHTAG_AUTHENTICATION_LEVEL = "BROADCASTER"
OPTIONS_POSITIVE_ARG = ("true", "on", "1", "t", "active")
TIMESTAMP_PATTERN = "%Y-%m-%dT%H:%M:%SZ"
CLIP_THANK_YOU_TEXT = (
    "A clip from the current stream #link Thanks to #user for clipping"
)
CLIP_WAIT_TIME = 2
CHECK_STREAM_INTERVAL = "60"
# TRACE, EXTDEBUG, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL
OPTIONS_LOG_LEVEL = ("EXTDEBUG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
LOG_LEVEL = "INFO"
STREAM_START_TIME_DIFFERENCE = "720"
