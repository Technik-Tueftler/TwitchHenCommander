# TwitchHenCommander
TwitchHenCommander is a bot that listens to configured twitch channel and collects hashtags from broadcaster, mod or vip in the chat. Finally, the broadcaster can post them on various platforms. Currently only post is supported on the DC.

[English readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.md)
 • [deutsche readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.de.md)

## Installation / Execution
1. locally runs the program by executing the main file. To do this, simply copy the repository and run `main.py`. Currently, first environment variables must be loaded into the IDE or environment. The login information can also be stored in ``/files/config.json``. The program was tested and developed under Python 3.11.
2. via a Docker container. Example see point ``Docker Compose Example`` below.

## What else is needed
- A twitch bot must be created via: https://dev.twitch.tv/console
- Discord WebHook connection, check `Supported platforms to broadcast`

## Supported platforms to broadcast
Currently only Discord is supported via WebHook. To do this, a new WebHook must be created in the server settings under Integration. Here you can also set the channel on which the notification should be sent.

## Environment variables
| Variable         | Explanation                                                    | Example                                         |
|------------------|----------------------------------------------------------------|-------------------------------------------------|
| TW_CLIENT_ID     | Twitch client ID for the bot.                                  | edr33sdfvbnmwsxdcfrt55jkdedded                  |
| TW_TOKEN         | Twitch token for the bot.                                      | hkedkodendoe343434gtgtdedexyde5667              |
| TW_NICKNAME      | Nickname of the bot as it is displayed in the chat.            | Technik_Tueftler                                |
| TW_INIT_CHANNELS | All channels that are to be observed, separated via a comma.   | technik_tueftler,thebrutzler                    |
| DC_USER_NAME     | User name of the WebHook in Discord.                           | HashtagBot                                      |
| DC_WEBHOOK_URL   | WebHook-URL from WebHook in Discord.                           | https://discord.com/api/webhooks/87364/oiehdied |

It is possible to start the bot without the environment variables. To do this, all the variables listed must be set in the configuration file. See the chapter Configuration file.  

## Commands
If nothing is set in config file, the standard commands are used:

| Command     | Explanation                                 |
|-------------|---------------------------------------------|
| !helphash   | List all commands for the Hashtag-Bot.      |
| !statushash | Get status of the bot if running or paused. |
| !starthash  | Start collecting hashtags.                  |
| !finishhash | Finish collecting hashtags and send them.   |
| !stophash   | Stop collecting and delete hashtags.        |

It's possible to replace the names of the commands via the configuration file.

## Additional feature
| Feature                   | Explanation                                | Setting                |
|---------------------------|--------------------------------------------|------------------------|
| Start bot by stream start | Starts collecting hashtags at stream start | Via configuration file |
| Lowercase hashtags        | Convert all hashtags to lowercase          | Via configuration file |

## Configuration file
the configuration file must be copied to the /files directory. You can use the example from the repository for this. The file is only necessary if you need the additional functionalities. The overview is in the list:
If nothing is set in config file, the standard commands are used:

| Variable                 | Explanation                                                               | Option                                 | value  |
|--------------------------|---------------------------------------------------------------------------|----------------------------------------|--------|
| client_id                | Twitch client ID for the bot.                                             | Optional, only if not via env variable | String |
| token                    | Twitch token for the bot.                                                 | Optional, only if not via env variable | String |
| nickname                 | Nickname of the bot as it is displayed in the chat.                       | Optional, only if not via env variable | String |
| init_channels            | All channels that are to be observed, separated via a comma.              | Optional, only if not via env variable | String |
| broadcaster_id           | Broadcaster ID of the bot                                                 | Optional, is fetched via nickname      | String |
| start_bot_at_streamstart | Starts collecting hashtags at stream start                                | Optional, only if needed               | bool   |
| start_bot_command        | Alternative command name to start the bot                                 | Optional, only if other desired        | String |
| finish_bot_command       | Alternative command name to finish the bot                                | Optional, only if other desired        | String |
| stop_bot_command         | Alternative command name to stop the bot                                  | Optional, only if other desired        | String |
| status_bot_command       | Alternative command name to get status of the bot                         | Optional, only if other desired        | String |
| help_bot_command         | Alternative command name to get help for the bot                          | Optional, only if other desired        | String |
| hashtag_max_length       | Maximum number of characters for a hashtag                                | optional, standard is 10 chars         | Int    |
| hashtag_min_length       | Maximum number of characters for a hashtag                                | optional, standard is 3 chars          | Int    |
| tweet_start_string       | Alternative text in front of the collected hashtags in the message        | Optional, standard is: Highlights:     | String |
| tweet_end_string         | Alternative text that appears after the collected hashtags in the message | Optional, standard is: Thanks!         | String |
| hashtag_all_lower_case   | All characters in the hashtag are converted to lowercase letters          | Optional, standard is false            | bool   |
| discord_username         | User name of the WebHook in Discord.                                      | Optional, only if not via env variable | String |
| webhook_url              | WebHook-URL from WebHook from Discord.                                    | Optional, only if not via env variable | String |

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