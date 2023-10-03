# TwitchHashtagBot
Der TwitchHashtagBot ist ein Bot, welcher auf konfigurierte Twitchkanäle hört und dort die Hashtags sammelt, welche vom Streamer, Mod oder Vip im Chat geschrieben wurde. Am Ende kann der Streamer diese auf konfigurierte Kanäle posten.

[deutsche readme](https://github.com/Technik-Tueftler/TwitchHashtagBot/blob/main/README.de.md)
 • [English readme](https://github.com/Technik-Tueftler/TwitchHashtagBot/blob/main/README.md)

## Installation / Ausführung
1. führt das Programm lokal aus, indem es die Hauptdatei ausführt. Dazu wird einfach das Repository kopiert und `main.py` ausgeführt. Derzeit müssen zunächst Umgebungsvariablen in die IDE oder Umgebung geladen werden. Die Logindaten könne auch in der ``/files/config.json`` abgelegt werden. Das Programm wurde unter Python 3.11 getestet und entwickelt.
2. über einen Docker-Container. Beispiel siehe Punkt ``Docker Compose Example`` unten.

## Was sonst noch benötigt wird
- Ein Twitch-Bot muss erstellt werden über: https://dev.twitch.tv/console

## Unterstützte Plattformen für die Übertragung
Derzeit wird nur Discord über WebHook unterstützt. Dazu muss in den Servereinstellungen unter Integration ein neuer WebHook angelegt werden. Hier können Sie auch den Kanal einstellen, auf dem die Benachrichtigung gesendet werden soll.

## Environment variables
| Variable         | Erklärung                                                            | Beispiel                                        |
|------------------|----------------------------------------------------------------------|-------------------------------------------------|
| TW_CLIENT_ID     | Twitch client ID vom Bot.                                            | edr33sdfvbnmwsxdcfrt55jkdedded                  |
| TW_TOKEN         | Twitch token vom Bot.                                                | hkedkodendoe343434gtgtdedexyde5667              |
| TW_NICKNAME      | Anzeigename des Bots im Chat.                                        | Technik_Tueftler                                |
| TW_INIT_CHANNELS | Alle Kanäle, die beobachtet werden sollen, getrennt durch ein Komma. | technik_tueftler,thebrutzler                    |
| DC_USER_NAME     | Username des WebHook im Discord.                                     | HashtagBot                                      |
| DC_WEBHOOK_URL   | WebHook-URL des WebHook im Discord.                                  | https://discord.com/api/webhooks/87364/oiehdied |

## Befehle
| Befehle     | Erklärung                                                   |
|-------------|-------------------------------------------------------------|
| !helpHash   | Listet alle Befehle des Hashtag-Bot auf.                    |
| !statusHash | Gibt den Status des Bots aus ob er läuft oder pausiert ist. |
| !startHash  | Beginnt das sammeln der Hashtags.                           |
| !finishHash | Beendet das sammeln und sendet die Hashtags.                |
| !stopHash   | Beendet das sammeln und löscht die Hashtags.                |

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