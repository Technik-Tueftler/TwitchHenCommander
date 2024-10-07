# TwitchHenCommander
The TwitchHenCommander is a program that listens to an adjustable Twitch chat and saves various things there and reacts to events. The exact functions are described in more detail under the heading `Functions`. The bot can be started locally in a Python environment or as a Docker container. More details under the heading `Installation / Execution`.

[English readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.md)
 • [deutsche readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.de.md)


## Summary Feature
1. Collect and post hashtags
2. Post new clips
3. Stream start message

## Feature
1. Collects hashtags in the broadcaster's Twitch chat and posts them to the configured Discord channel at the end of the stream or when a command is executed. It can be set that only hashtags with a configurable rank are collected (Vips, Mods, Broadcaster). You can also specify whether the hashtag function should be started or ended with the start or end of the stream and thus be posted automatically.
2. If a new clip is created in your stream, it can also be posted on the Discord channel. 
3. When your stream starts, a message is sent to the Discord channel. You can customize this message and pass parameters.
4. Suppressing hashtags for the post via a blacklist and adding them via a command


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

| Variable | Explanation | Example |
|----------|-------------|---------|
| TW_CLIENT_ID | Twitch client ID of Bot. | edr33sdfvbnmwsxdcfrt55jkdedded |
| TW_TOKEN | Twitch token of Bot. | hkedkodendoe343434gtgtdedexyde5667 |
| TW_NICKNAME | Display name of the bot in the chat. | Technik_Tueftler |
| TW_INIT_CHANNELS | All channels to be monitored, separated by a comma. | technik_tueftler,thebrutzler |
| TW_BROADCASTER_ID | The ID of the broadcaster, optional, is also determined automatically. | 123456789 |
| CHECK_STREAM_INTERVAL | Time (s) in whether the stream is online or offline. | 60                                              |
| LOG_LEVEL | Defines the level of log messages and which are to be output and saved. | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| START_BOT_AT_STREAMSTART | Defines whether the bot should be started when stream starts. | `active` for active or nothing for inactive |
| FINISH_BOT_AT_STREAMEND | Defines whether the bot should be terminated at the end of stream. | `active` for active or nothing for inactive |

### Hashtag function
All variables are described here, which are required to collect hashtags and post them in the Discord at the end.
| Variable | Explanation | Example |
|----------|-------------|---------|
| DC_FEATURE_HASHTAG | Determines whether the function should be active or not. | `active` for active or nothing for inactive |
| DC_USER_NAME_HASHTAG | Username of WebHook in Discord for posting Hashtags. | HashtagBot |
| DC_WEBHOOK_URL_HASHTAG | WebHook-URL of WebHook ii Discord for posting Hashtags. | https://discord.com/api/webhooks/87364/oiehdied |
| HASHTAG_MAX_LENGTH | Defines the maximum length of a hashtag. | 20 |
| HASHTAG_MIN_LENGTH | Defines the minimum length of a hashtag. | 3  |
| TWEET_MAX_LENGTH | Currently has no function | NA |
| HASHTAG_CHATTER_THANKS_TEXT | Defines the text that appears when the stream ends | See **Set own text** |
| HASHTAG_ALL_LOWER_CASE | Determines whether all hashtags are converted to lowercase letters. | `active` for active or nothing for inactive |
| HASHTAG_AUTHENTICATION_LEVEL | Defines minimum rank which hashtags should be posted. | Possible: EVERYONE, SUBSCRIBER, VIP, MOD, BROADCASTER |
| HASHTAG_FEATURE_FROM_STREAM_TAGS|Determines whether the stream tags should be added in the hashtag list when the stream starts|`active` for active or nothing for inactive|


### Clip function
All variables that are required to recognize clips and post them in the Discord are described here.
| Variable | Explanation | Example |
|----------|-------------|---------|
| DC_FEATURE_CLIPS | Determines whether the function should be active or not. | `active` for active or nothing for inactive |
| DC_USER_NAME_CLIP | Username of WebHook in Discord to post new clips. | ClipBot |
| DC_WEBHOOK_URL_CLIP | WebHook-URL of WebHook in Discord to post new clips. | https://discord.com/api/webhooks/87364/oiehttedied |
| CLIPS_FETCH_TIME | Time (s) to check whether a new clip has been created. | 60 |
| CLIP_THANK_YOU_TEXT | Defines a text that appears when a new clip is posted. | See **Set own text** |


### Stream-Start function
All variables that are required to post a message at the beginning of a stream in the Discord are described here.
| Variable | Explanation | Example |
|----------|-------------|---------|
| DC_FEATURE_MESSAGE_STREAMSTART | Determines whether the function should be active or not. | `active` for active or nothing for inactive |
| DC_USER_NAME_MESSAGE_STREAMSTART | Username of WebHook in Discord to post message. | UpdateBot |
| DC_WEBHOOK_URL_MESSAGE_STREAMSTART | WebHook-URL of WebHook in Discord to post message. | https://discord.com/api/webhooks/87364/oiehtt |
| DC_FEATURE_MESSAGE_STREAMSTART_TEXT | Defines a start text that appears during stream start. | Siehe **Festlegen eigener Text** |


### Befehle
If no commands are defined in the environment variables, the default commands are used. If you want to rename these, the corresponding variable must be adapted. The exclamation mark is always used as the identifier.

| Default command   | Explanation                                                   | environment variable       |
|-------------------|---------------------------------------------------------------|----------------------------|
| !helphash         | Lists all commands of the hashtag bot.                        | BOT_HASHTAG_COMMAND_HELP   |
| !statushash       | Shows the status of the bot, whether it is running or paused. | BOT_HASHTAG_COMMAND_STATUS |
| !starthash        | Start collecting the hashtags.                                | BOT_HASHTAG_COMMAND_START  |
| !finishhash       | Finish collecting and send the hashtags.                      | BOT_HASHTAG_COMMAND_FINISH |
| !stophash         | Stop collecting and delete the hashtags.                      | BOT_HASHTAG_COMMAND_STOP   |
| !hashblacklist    | Add hashtag to blacklist.                                     | BOT_HASHTAG_COMMAND_BANN   |


## Set own text
For some texts, it is possible to replace placeholders with your own variables and thus create a configurable text.  This means that the placeholders always remain the same and can be integrated into your own text.  
|Placeholder|Variable|Meaning|
|--------|-----------|---------|
|#broadcaster|DC_FEATURE_MESSAGE_STREAMSTART_TEXT| Name of streamer|
|#genre|DC_FEATURE_MESSAGE_STREAMSTART_TEXT|Genre of game|
|#link|DC_FEATURE_MESSAGE_STREAMSTART_TEXT|Link to streamer channel|
|#link|CLIP_THANK_YOU_TEXT|Link to the clip you just created|
|#user|CLIP_THANK_YOU_TEXT|Chatter who created the clip|
|#chatter_all|HASHTAG_CHATTER_THANKS_TEXT|All chatters who had posted a hashtag|
|#chatter_except_last|HASHTAG_CHATTER_THANKS_TEXT|All chatters who had posted a hashtag except the last one on the list|
|#chatter_last|HASHTAG_CHATTER_THANKS_TEXT|The last chatter from the list who had posted a hashtag|

**Example clip:** A clip from the current stream #link Thanks to #user for clipping.
**Example hashtag:** Highlights from stream: #hashtags, thanks to #chatter_except_last and #chatter_last for creating the highlights!"
**Example stream-start-message:** #broadcaster with #genre is online. It's amazing what's happen here: #link

## Suppressing hashtags
There is the option of not registering hashtags for the post and adding them to a blacklist. All hashtags are in the file **blacklist.txt** and can be added there manually before the bot starts. While the bot is running, this is possible at any time via the chat command and is also entered in the text document.  


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