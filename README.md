# TwitchHenCommander
TwitchHenCommander is a bot that listens to configured twitch channels and collects hashtags from broadcaster, mod or vip in the chat. Finally, the broadcaster can post them on various platforms.

[English readme](https://github.com/Technik-Tueftler/TwitchHashtagBot/blob/main/README.md)
 • [deutsche readme](https://github.com/Technik-Tueftler/TwitchHashtagBot/blob/main/README.de.md)

## Installation / Execution
1. locally runs the program by executing the main file. To do this, simply copy the repository and run `main.py`. Currently, first environment variables must be loaded into the IDE or environment. The login information can also be stored in ``/files/config.json``. The program was tested and developed under Python 3.11.
2. via a Docker container. Example see point ``Docker Compose Example`` below.

## What else is needed
- A twitch bot must be created via: https://dev.twitch.tv/console

## Supported platforms to broadcast
Currently only Discord is supported via WebHook. To do this, a new WebHook must be created in the server settings under Integration. Here you can also set the channel on which the notification should be sent.

## Environment variables
|Variable| Explanation                                                  | Example                                         |
|---|--------------------------------------------------------------|-------------------------------------------------|
|TW_CLIENT_ID| Twitch client ID for the bot.                                | edr33sdfvbnmwsxdcfrt55jkdedded                  |
|TW_TOKEN| Twitch token for the bot.                                    | hkedkodendoe343434gtgtdedexyde5667              |
|TW_NICKNAME| Nickname of the bot as it is displayed in the chat.          | Technik_Tueftler                                |
|TW_INIT_CHANNELS| All channels that are to be observed, separated via a comma. | technik_tueftler,thebrutzler                    |
|DC_USER_NAME| User name of the WebHook in Discord.                         | HashtagBot                                      |
|DC_WEBHOOK_URL| WebHook-URL from WebHook from Discord.                       | https://discord.com/api/webhooks/87364/oiehdied |

## Commands
| Command     | Explanation                                 |
|-------------|---------------------------------------------|
| !helpHash   | List all commands for the Hashtag-Bot.      |
| !statusHash | Get status of the bot if running or paused. |
| !startHash  | Start collecting hashtags.                  |
| !finishHash | Finish collecting hashtags and send them.   |
| !stopHash   | Stop collecting and delete hashtags.        |

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