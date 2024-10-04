# TwitchHenCommander
Der TwitchHenCommander ist ein Programm, der auf einen einstellbaren Twitchchat hört und dort verschiedene Dinge speichert und auf Events reagiert. Die genauen Funktionen sind unter der Überschrift `Funktionen` genauer beschrieben. Der Bot kann Local in einer Python Umgebung gestartet werden oder als Docker Container. Näheres unter der Überschrift `Installation / Ausführung`.

[deutsche readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.de.md)
 • [English readme](https://github.com/Technik-Tueftler/TwitchHenCommander/blob/main/README.md)

## Zusammenfassung Funktionen
1. Sammeln und posten von Hashtags
2. Neue Clips posten
3. Streamstart Nachricht posten

## Funktionen
1. Sammelt Hashtags im Twitchchat des Broadcasters und posted diese am Ende des Streams oder beim ausführen eines Befehls in den konfigurierten Discord Channel. Es kann eingestellt werden, dass nur Hashtags gesammelt werden, die einen einstellbaren Rang haben (Vips, Mods, Broadcaster). Des Weiteren kann festgelegt werden, ob die Hashtag-Funktion mit dem Stream-Start bzw. Stream-Ende gestartet bzw. beendet werden soll und damit automatisch gepostet werden soll.
2. Wird ein neuer Clip in eurem stream erstellt, kann dieser auch auf dem Discord Channel gepostet werden. 
3. Wenn euer Stream startet, wird eine Nachricht in den Discord Channel gesendet. Diese Nachricht kann man anpassen und Parameter übergeben.
4. Unterdrücken von Hashtags für den Post über eine Blacklist und hinzufügen über einen Befehl


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
| Variable | Erklärung | Beispiel |
|----------|-----------|----------|
| TW_CLIENT_ID | Twitch client ID vom Bot. | edr33sdfvbnmwsxdcfrt55jkdedded |
| TW_TOKEN | Twitch token vom Bot. | hkedkodendoe343434gtgtdedexyde5667 |
| TW_NICKNAME | Anzeigename des Bots im Chat. | Technik_Tueftler |
| TW_INIT_CHANNELS | Alle Kanäle, die beobachtet werden sollen, getrennt durch ein Komma. | technik_tueftler,thebrutzler |
| TW_BROADCASTER_ID | Die ID des Broadcasters, optional, wird auch automatisch ermittelt.  | 123456789 |
| CHECK_STREAM_INTERVAL | Zeit (s) in geschaut wird, ob der Stream online oder offline ist. | 60 |
| LOG_LEVEL | Legt das Level der Log-Nachrichten fest und welche gespeichert werden sollen. | DEBUG, INFO, WARNING, ERROR, CRITICAL |
| START_BOT_AT_STREAMSTART | Legt fest, ob der Bot beim Streamstart gestartet werden soll. | `active` für aktiv oder nichts für inactiv |
| FINISH_BOT_AT_STREAMEND  | Legt fest, ob der Bot beim Streamende beendet werden soll. | `active` für aktiv oder nichts für inactiv |

### Hashtag Funktion
Hier werden alle Variablen beschrieben, welche benötigt werden um Hashtags zu sammeln und am Ende im Discord zu posten.
| Variable | Erklärung | Beispiel |
|----------|-----------|----------|
| DC_FEATURE_HASHTAG | Legt fest, ob die Funktion aktiv sein soll oder nicht. | `active` für aktiv oder nichts für inactiv |
| DC_USER_NAME_HASHTAG | Username des WebHook im Discord zum posten der Hashtags. | HashtagBot |
| DC_WEBHOOK_URL_HASHTAG | WebHook-URL des WebHook im Discord zum posten der Hashtags. | https://discord.com/api/webhooks/87364/oiehdied |
| HASHTAG_MAX_LENGTH | Legt fest was die maximale Länge eines Hashtags ist. | 20 |
| HASHTAG_MIN_LENGTH | Legt fest was die minimale Länge eines Hashtags ist. | 3 |
| TWEET_MAX_LENGTH | Hat aktuell keine Funktion | NA                                                        |
| HASHTAG_CHATTER_THANKS_TEXT | Legt den Text fest, der kommt, wenn der Stream beendet wird. | Siehe **Festlegen eigener Text** |
| HASHTAG_ALL_LOWER_CASE | Legt fest, ob alle Hashtags in Kleinbuchstaben umgewandelt werden. | `active` für aktiv oder nichts für inactiv |
| HASHTAG_AUTHENTICATION_LEVEL | Legt die Rolle fest für das posten von Hashtags. | Möglich sind: EVERYONE, SUBSCRIBER, VIP, MOD, BROADCASTER |


### Clip Funktion
Hier werden alle Variablen beschrieben, welche benötigt werden um Clips zu erkennen und im Discord zu posten.
| Variable | Erklärung | Beispiel |
|----------|-----------|----------|
| DC_FEATURE_CLIPS | Legt fest, ob die Funktion aktiv sein soll oder nicht. | `active` für aktiv oder nichts für inactiv |
| DC_USER_NAME_CLIP | Username des WebHook im Discord zum posten neuer Clips. | ClipBot |
| DC_WEBHOOK_URL_CLIP | WebHook-URL des WebHook im Discord zum posten neuer Clips. | https://discord.com/api/webhooks/87364/oiehttedied |
| CLIPS_FETCH_TIME | Zeit (s) in geschaut wird, ob ein neuer Clip erstellt wurde. | 60 |
| CLIP_THANK_YOU_TEXT | Legt einen Starttext fest, der kommt, wenn ein neuer Clip gepostet wird. | Siehe **Festlegen eigener Text** |

### Streamstart Nachricht Funktion
Hier werden alle Variablen beschrieben, welche benötigt werden um eine Nachricht am Anfang eines Streams im Discord zu posten.
| Variable | Erklärung | Beispiel |
|----------|-----------|----------|
| DC_FEATURE_MESSAGE_STREAMSTART | Legt fest, ob die Funktion aktiv sein soll oder nicht. | `active` für aktiv oder nichts für inactiv |
| DC_USER_NAME_MESSAGE_STREAMSTART | Username des WebHook im Discord zum posten der Nachricht. | UpdateBot |
| DC_WEBHOOK_URL_MESSAGE_STREAMSTART | WebHook-URL des WebHook im Discord. | https://discord.com/api/webhooks/87364/oiehttedied |
| DC_FEATURE_MESSAGE_STREAMSTART_TEXT | Legt den Text fest, der bei Streamstart gepostet wird. | Siehe **Festlegen eigener Text** |

### Befehle
Wenn keine Befehle in den environment Variablen festgelegt werden, werden die Standardbefehle. Möchte man diese umbenennen, muss die entsprechende variable angepasst werden. Das Erkennunszeichen ist dabei immer das Ausrufezeichen.

| Standard Befehle | Erklärung                                                   | environment Variable       |
|------------------|-------------------------------------------------------------|----------------------------|
| !helphash        | Listet alle Befehle des Hashtag-Bot auf.                    | BOT_HASHTAG_COMMAND_HELP   |
| !statushash      | Gibt den Status des Bots aus ob er läuft oder pausiert ist. | BOT_HASHTAG_COMMAND_STATUS |
| !starthash       | Beginnt das sammeln der Hashtags.                           | BOT_HASHTAG_COMMAND_START  |
| !finishhash      | Beendet das sammeln und sendet die Hashtags.                | BOT_HASHTAG_COMMAND_FINISH |
| !stophash        | Beendet das sammeln und löscht die Hashtags.                | BOT_HASHTAG_COMMAND_STOP   |
| !hashblacklist   | Hinzufügen von Hashtags zur Blacklist.                      | BOT_HASHTAG_COMMAND_BANN   |


## Festlegen eigener Text
Es gibt bei einigen Texten die Möglichkeit Platzhalter durch eigene Variablen zu ersetzen und so einen konfigurierbaren Text zu erstellen.  So bleiben die Platzhalter immer gleich und können in den eigenen Text eingebaut werden.  
|Platzhalter|Variable|Bedeutung|
|--------|-----------|---------|
|#broadcaster|DC_FEATURE_MESSAGE_STREAMSTART_TEXT|Name des Streamers|
|#genre|DC_FEATURE_MESSAGE_STREAMSTART_TEXT|Genre des Streams|
|#link|DC_FEATURE_MESSAGE_STREAMSTART_TEXT|Link zum Kanal|
|#link|CLIP_THANK_YOU_TEXT|Link zum gerade erstellten Clip|
|#user|CLIP_THANK_YOU_TEXT|Chatter der den Clip erstellt hat|
|#chatter_all|HASHTAG_CHATTER_THANKS_TEXT|Alle Chatter die einen Hashtag gepostet hatten|
|#chatter_except_last|HASHTAG_CHATTER_THANKS_TEXT|Alle Chatter die einen Hashtag gepostet hatten außer den letzten aus der Liste|
|#chatter_last|HASHTAG_CHATTER_THANKS_TEXT|Der letzte Chatter aus der Liste der einen Hashtag gepostet hat|

**Beispiel Clip:** A clip from the current stream #link Thanks to #user for clipping.
**Beispiel Hashtag:** Highlights from stream: #hashtags, thanks to #chatter_except_last and #chatter_last for creating the highlights!"
**Beispiel Stream-Start-Nachricht:** #broadcaster with #genre is online. It's amazing what's happen here: #link

## Unterdrücken von Hashtags
Es gibt die Möglichkeit Hashtags für den Post nicht zu Registrieren und diese auf eine Blacklist zu nehmen. Alle Hashtags stehen in der Datei **blacklist.txt** und können dort vor dem Botstart manuell hinzugefügt werden. Während der Bot läuft ist dies jederzeit über den Chat-Befehl möglich und werden auch in das Textdokument eingetragen.  


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