# TwitchHenCommander
Der TwitchHenCommander ist ein Programm, der auf einen einstellbaren Twitchchat hört und dort verschiedene Dinge speichert und auf Events reagiert. Die genauen Funktionen sind unter der Überschrift `Funktionen` genauer beschrieben. Der Bot kann Local in einer Python Umgebung gestartet werden oder als Docker Container. Näheres unter der Überschrift `Installation / Ausführung`.

[deutsche readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.de.md)
 • [English readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.md)

## Funktionen
1. Sammelt Hashtags im Twitchchat des Broadcasters und posted diese am Ende des Streams oder beim ausführen eines Befehls in den konfigurierten Discord Channel. Es kann eingestellt werden, dass nur Hashtags gesammelt werden, die einen einstellbaren Rang haben (Vips, Mods, Broadcaster). Des Weiteren kann festgelegt werden, ob die Hashtag-Funktion mit dem Stream-Start bzw. Stream-Ende gestartet bzw. beendet werden soll und damit automatisch gepostet werden soll.
2. Wird ein neuer Clip erstellt in eurem Stream, kann dieser auch auf dem Discord gepostet werden.

## Installation / Ausführung
1. Führt das Programm lokal aus, indem es die Hauptdatei ausführt. Dazu wird einfach das Repository kopiert und `main.py` ausgeführt. Die Einstellungen müssen über die Umgebungsvariablen geladen werden. Dazu können die Variablen direkt im System hinterlegt sein oder man benutzt eine `.env` Datei. Hierzu kann die `template.env` Datei benutzt werden, indem man diese in `.env` umbenennt und in die benötigten Variablen den Wert schreibt. Das Programm wurde erstellt und getestet unter Python 3.11.
2. Über einen Docker-Container. Beispiel siehe Punkt ``Docker Compose Example`` unten.

## Was sonst noch benötigt wird
- Ein Twitch-Bot muss erstellt werden über: https://dev.twitch.tv/console
- Discord WebHook Verbindungen, siehe `Unterstützte Plattformen für die Übertragung`

## Unterstützte Plattformen für die Übertragung
Derzeit wird nur Discord über WebHook unterstützt. Dazu muss in den Servereinstellungen unter `Integration` ein neuer WebHook angelegt werden. Hier können Sie auch den Kanal einstellen, auf dem die Benachrichtigung gesendet werden soll.

## Environment variables
Nachfolgend werden alle Environment Variablen aufgelistet, welche für die jeweilige Funktion benötigt werden.

### Twitch Chat
Alle Variablen die benötigt werden um den Twitch Chat zu lesen.
| Variable                 | Erklärung                                                            | Beispiel                                        |
|--------------------------|----------------------------------------------------------------------|-------------------------------------------------|
| TW_CLIENT_ID             | Twitch client ID vom Bot.                                            | edr33sdfvbnmwsxdcfrt55jkdedded                  |
| TW_TOKEN                 | Twitch token vom Bot.                                                | hkedkodendoe343434gtgtdedexyde5667              |
| TW_NICKNAME              | Anzeigename des Bots im Chat.                                        | Technik_Tueftler                                |
| TW_INIT_CHANNELS         | Alle Kanäle, die beobachtet werden sollen, getrennt durch ein Komma. | technik_tueftler,thebrutzler                    |
| TW_BROADCASTER_ID        | Die ID des Broadcasters, optional, wird auch automatisch ermittelt.  | 123456789                                       |
| CHECK_STREAM_INTERVAL    | Zeit (s) in geschaut wird, ob der Stream online oder offline ist.    | 60                                              |
| START_BOT_AT_STREAMSTART | Legt fest, ob der Bot beim Streamstart gestartet werden soll.        | `active` für aktiv oder nichts für inactiv      |
| FINISH_BOT_AT_STREAMEND  | Legt fest, ob der Bot beim Streamende beendet werden soll.           | `active` für aktiv oder nichts für inactiv      |

# Hashtag Funktion
Hier werden alle Variablen beschrieben, welche benötigt werden um Hashtags zu sammeln und am Ende im Discord zu posten.
| Variable                     | Erklärung                                                             | Beispiel                                                  |
|------------------------------|-----------------------------------------------------------------------|-----------------------------------------------------------|
| DC_FEATURE_HASHTAG           | Legt fest, ob die Funktion aktiv sein soll oder nicht.                | `active` für aktiv oder nichts für inactiv                |
| DC_USER_NAME_HASHTAGc        | Username des WebHook im Discord.                                      | HashtagBot                                                |
| DC_WEBHOOK_URL_HASHTAG       | WebHook-URL des WebHook im Discord.                                   | https://discord.com/api/webhooks/87364/oiehdied           |
| HASHTAG_MAX_LENGTH           | Legt fest was die maximale Länge eines Hashtags ist.                  | 20                                                        |
| HASHTAG_MIN_LENGTH           | Legt fest was die minimale Länge eines Hashtags ist.                  | 3                                                         |
| TWEET_MAX_LENGTH             | Hat aktuell keine Funktion                                            | NA                                                        |
| TWEET_START_STRING           | Legt einen Text fest, der vor den Hashtags geschrieben wird.          | Das waren die Hashtags aus dem Stream:                    |
| TWEET_END_STRING             | Legt einen Text fest, der nach den Hashtags geschrieben wird.         | Danke, dass ihr dabei wart.                               |
| HASHTAG_ALL_LOWER_CASE       | Legt fest, ob alle Hashtags in Kleinbuchstaben umgewandelt werden.    | `active` für aktiv oder nichts für inactiv                |
| HASHTAG_AUTHENTICATION_LEVEL | Legt den minimalen Rang fest, welche Hashtags gepostet werden sollen. | Möglich sind: EVERYONE, SUBSCRIBER, VIP, MOD, BROADCASTER |

## Befehle
Wenn keine Befehle in der Konfigurationsdatei gesetzt werden, werden die folgenden Standardbefehle gesetzt:

| Befehle     | Erklärung                                                   |
|-------------|-------------------------------------------------------------|
| !helphash   | Listet alle Befehle des Hashtag-Bot auf.                    |
| !statushash | Gibt den Status des Bots aus ob er läuft oder pausiert ist. |
| !starthash  | Beginnt das sammeln der Hashtags.                           |
| !finishhash | Beendet das sammeln und sendet die Hashtags.                |
| !stophash   | Beendet das sammeln und löscht die Hashtags.                |

Es ist möglich die Namen der Befehle über die Konfigurationsdatei zu ersetzen.  

## Zusätzliche Funktionen
| Funktion                   | Erklärung                                        | Einstellung                  |
|----------------------------|--------------------------------------------------|------------------------------|
| Botstart bei Streamstart   | Startet das sammeln der Hashtags bei Streamstart | Über die Konfigurationsdatei |
| Lowercase hashtags         | Convert all hashtags to lowercase                | Über die Konfigurationsdatei |

## Konfigurationsdatei
Die Konfigurationsdatei muss in das Verzeichnis /files kopiert werden. Hierzu kannst du das Beispiel aus dem Repository benutzen. Die Datei ist nur nötig, wenn du die Zusatzfunktionalitäten brauchst. In der Liste ist der Überblick.

| Variable                 | Erklärung                                                                 | Option                                     | Wert   |
|--------------------------|---------------------------------------------------------------------------|--------------------------------------------|--------|
| client_id                | Twitch client ID vom Bot.                                                 | Optional, nur wenn nicht über env Variable | String |
| token                    | Twitch token vom Bot.                                                     | Optional, nur wenn nicht über env Variable | String |
| nickname                 | Anzeigename des Bots im Chat.                                             | Optional, nur wenn nicht über env Variable | String |
| init_channels            | Alle Kanäle, die beobachtet werden sollen, getrennt durch ein Komma.      | Optional, nur wenn nicht über env Variable | String |
| broadcaster_id           | Broadcaster ID des Bots                                                   | Optional, wird über Kanalname abgefragt    | String |
| start_bot_at_streamstart | Starts collecting hashtags at stream start                                | Optional, nur wenn gebraucht               | bool   |
| start_bot_command        | Alternative command name to start the bot                                 | Optional, nur wenn anderer gewollt         | String |
| finish_bot_command       | Alternative command name to finish the bot                                | Optional, nur wenn anderer gewollt         | String |
| stop_bot_command         | Alternative command name to stop the bot                                  | Optional, nur wenn anderer gewollt         | String |
| status_bot_command       | Alternative command name to get status of the bot                         | Optional, nur wenn anderer gewollt         | String |
| help_bot_command         | Alternative command name to get help for the bot                          | Optional, nur wenn anderer gewollt         | String |
| hashtag_max_length       | Maximum number of characters for a hashtag                                | optional, Standard ist 10 Zeichen          | Int    |
| hashtag_min_length       | Maximum number of characters for a hashtag                                | optional, Standard ist 10 Zeichen          | Int    |
| tweet_start_string       | Alternative text in front of the collected hashtags in the message        | Optional, Standard ist: Highlights:        | String |
| tweet_end_string         | Alternative text that appears after the collected hashtags in the message | Optional, Standard ist: Thanks!            | String |
| hashtag_all_lower_case   | All characters in the hashtag are converted to lowercase letters          | Optional, Standard ist: false              | bool   |
| discord_username         | Username des WebHook im Discord.                                          | Optional, nur wenn nicht über env Variable | String |
| webhook_url              | WebHook-URL des WebHook im Discord.                                       | Optional, nur wenn nicht über env Variable | String |

## Docker Compose Beispiel
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