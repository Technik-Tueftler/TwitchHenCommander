# TwitchHenCommander
The TwitchHenCommander is a program that listens to an adjustable Twitch chat and saves various things there and reacts to events. The exact functions are described in more detail under the heading `Functions`. The bot can be started locally in a Python environment or as a Docker container. More details under the heading `Installation / Execution`.

[English readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.md)
 • [deutsche readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.de.md)

## Feature
1. Collects hashtags in the broadcaster's twitch chat and posts them to the configured Discord channel at the end of the stream or when a command is executed. You can set that only hashtags with a configurable rank are collected (vips, mods, broadcasters). You can also specify whether the hashtag function should be started or ended with the start or end of the stream and thus be posted automatically.
2. If a new clip is created in your stream, it can also be posted on the Discord.

## Installation / Execution
1. Runs the program locally by executing the main file. To do this, simply copy the repository and execute `main.py`. The settings must be loaded via the environment variables. The variables can be stored directly in the system or you can use an `.env` file. The `template.env` file can be used for this by renaming it to `.env` and writing the value to the required variables. The program was tested and developed under Python 3.11.
2. via a Docker container. Example see point ``Docker Compose Example`` below.

## What else is needed
- A twitch bot must be created via: https://dev.twitch.tv/console
- Discord WebHook connection, check `Supported platforms to broadcast`

## Supported platforms to broadcast
Currently only Discord is supported via WebHook. To do this, a new WebHook must be created in the server settings under `Integration`. Here you can also set the channel on which the notification should be sent.

## Environment variables
All environment variables required for the respective function are listed below.

### Twitch Chat
All variables needed to read the Twitch chat.

| Variable                 | Explanation                                                            | Example                                         |
|--------------------------|------------------------------------------------------------------------|-------------------------------------------------|
| TW_CLIENT_ID             | Twitch client ID of Bot.                                               | edr33sdfvbnmwsxdcfrt55jkdedded                  |
| TW_TOKEN                 | Twitch token of Bot.                                                   | hkedkodendoe343434gtgtdedexyde5667              |
| TW_NICKNAME              | Display name of the bot in the chat.                                   | Technik_Tueftler                                |
| TW_INIT_CHANNELS         | All channels to be monitored, separated by a comma.                    | technik_tueftler,thebrutzler                    |
| TW_BROADCASTER_ID        | The ID of the broadcaster, optional, is also determined automatically. | 123456789                                       |
| CHECK_STREAM_INTERVAL    | Time (s) in whether the stream is online or offline.                   | 60                                              |
| START_BOT_AT_STREAMSTART | Defines whether the bot should be started when the stream starts.      | `active` for active or nothing for inactive     |
| FINISH_BOT_AT_STREAMEND  | Defines whether the bot should be terminated at the end of the stream. | `active` for active or nothing for inactive     |

### Hashtag function
All variables are described here, which are required to collect hashtags and post them in the Discord at the end.
| Variable                     | Explanation                                                         | Example                                                   |
|------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------|
| DC_FEATURE_HASHTAG           | Determines whether the function should be active or not.            | `active` for active or nothing for inactive               |
| DC_USER_NAME_HASHTAG         | Username of WebHook in Discord.                                     | HashtagBot                                                |
| DC_WEBHOOK_URL_HASHTAG       | WebHook-URL of WebHook ii Discord.                                  | https://discord.com/api/webhooks/87364/oiehdied           |
| HASHTAG_MAX_LENGTH           | Defines the maximum length of a hashtag.                            | 20                                                        |
| HASHTAG_MIN_LENGTH           | Defines the minimum length of a hashtag.                            | 3                                                         |
| TWEET_MAX_LENGTH             | Currently has no function                                           | NA                                                        |
| TWEET_START_STRING           | Defines a text that is written before the hashtags.                 | These were the hashtags from the stream:                  |
| TWEET_END_STRING             | Defines a text that is written after the hashtags.                  | Thank you for being there.                                |
| HASHTAG_ALL_LOWER_CASE       | Determines whether all hashtags are converted to lowercase letters. | `active` for active or nothing for inactive               |
| HASHTAG_AUTHENTICATION_LEVEL | Defines the minimum rank which hashtags should be posted.           | Possible: EVERYONE, SUBSCRIBER, VIP, MOD, BROADCASTER     |


### Clip function
All variables that are required to recognize clips and post them in the Discord are described here.
| Variable                    | Explanation                                                  | Example                                                  |
|-----------------------------|--------------------------------------------------------------|----------------------------------------------------------|
| DC_FEATURE_CLIPS            | Determines whether the function should be active or not.     | `active` for active or nothing for inactive              |
| DC_USER_NAME_CLIP           | Username of WebHook in Discord.                              | ClipBot                                                  |
| DC_WEBHOOK_URL_CLIP         | WebHook-URL of WebHook in Discord.                           | https://discord.com/api/webhooks/87364/oiehttedied       |
| CLIPS_FETCH_TIME            | Time (s) to check whether a new clip has been created.       | 60                                                       |
| DEFAULT_CLIP_THANK_YOU_TEXT | Defines a start text that appears when a new clip is posted. | Clip from the current stream:                            |

### Befehle
If no commands are defined in the environment variables, the default commands are used. If you want to rename these, the corresponding variable must be adapted. The exclamation mark is always used as the identifier.

| Default command   | Explanation                                                   | environment variable       |
|-------------------|---------------------------------------------------------------|----------------------------|
| !helphash         | Lists all commands of the hashtag bot.                        | BOT_HASHTAG_COMMAND_HELP   |
| !statushash       | Shows the status of the bot, whether it is running or paused. | BOT_HASHTAG_COMMAND_STATUS |
| !starthash        | Start collecting the hashtags.                                | BOT_HASHTAG_COMMAND_START  |
| !finishhash       | Finish collecting and send the hashtags.                      | BOT_HASHTAG_COMMAND_FINISH |
| !stophash         | Stop collecting and delete the hashtags.                      | BOT_HASHTAG_COMMAND_STOP   |

## Docker Compose Example
````commandline
version: "2"
services:
  influxdb:
    image: techniktueftler/twitchhashtagbot:latest
    container_name: tetue_twitch_hashtag_bot
    volumes:
      - /srv/dev-disk-by-uuid-0815-1234-123-456-0815/data/tetue_twitch_hashtag_bot/:/user/app/TwitchHashtagBot/files/
    environment:
      - TW_CLIENT_ID=edr33sdfvbnmwsxdcfrt55jkdedded
      - TW_TOKEN=hkedkodendoe343434gtgtdedexyde5667
      - TW_NICKNAME=Technik_Tueftler
      - TW_INIT_CHANNELS=technik_tueftler
      - DC_USER_NAME=HashtagBot
      - DC_WEBHOOK_URL=https://discord.com/api/webhooks/87364/oiehdied
````