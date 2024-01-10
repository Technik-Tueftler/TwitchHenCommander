"""
File contains all constants for easy central import and usage.
"""
CONFIGURATION_FILE_PATH = "../files/config.json"
HASHTAG_FILE_PATH = "../files/hashtags.txt"
LOG_FILE_PATH = "../files/log.txt"
HASHTAG_MAX_LENGTH = 10
HASHTAG_MIN_LENGTH = 3
TWEET_MAX_LENGTH = 280
TWEET_START_STRING = "Highlights aus dem Stream: "
TWEET_END_STRING = "Danke, dass ihr heute da wart."
HASHTAG_ALL_LOWER_CASE = False
TWITCH_WEBSOCKET_URL = "wss://eventsub.wss.twitch.tv/ws"
TWITCH_SUBSCRIPTION_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"
REQUEST_TIMEOUT = 10
BOT_HASHTAG_COMMAND_START = "starthash"
BOT_HASHTAG_COMMAND_FINISH = "finishhash"
BOT_HASHTAG_COMMAND_STOP = "stophash"
BOT_HASHTAG_COMMAND_STATUS = "statushash"
BOT_HASHTAG_COMMAND_HELP = "helphash"
