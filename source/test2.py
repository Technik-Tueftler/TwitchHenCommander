import os
import json
import asyncio
from pprint import pprint
from websockets.sync.client import connect
import requests

client_id = os.getenv("TW_CLIENT_ID", None)
token = os.getenv("TW_TOKEN", None)


async def listener():
    # den Port kann man weglassen, ist default
    url = "wss://eventsub.wss.twitch.tv/ws?keepalive_timeout_seconds=30"
    # url = "wss://eventsub.wss.twitch.tv/ws"
    post_url = "https://api.twitch.tv/helix/eventsub/subscriptions"
    with connect(url) as websocket:
        welcome_message = json.loads(websocket.recv())
        print(welcome_message)
        websocket_id = welcome_message["payload"]["session"]["id"]
        subscriptions_message = {
            "type": "stream.online",
            "version": "1",
            "condition": {
                "broadcaster_user_id": "206130928"
            },
            "transport": {
                "method": "websocket",
                "session_id": websocket_id
            }
        }
        headers = {
            "Client-ID": client_id, 
            "Authorization": f"Bearer {token}"
            }
        response = requests.post(post_url, json=subscriptions_message, headers=headers, timeout=20)
        print(response.json())
        subscriptions_message = {
            "type": "channel.follow",
            "version": "2",
            "condition": {
                "broadcaster_user_id": "206130928",
                "moderator_user_id": "206130928"
            },
            "transport": {
                "method": "websocket",
                "session_id": websocket_id
            }
        }
        headers = {
            "Client-ID": client_id, 
            "Authorization": f"Bearer {token}"
            }
        response = requests.post(post_url, json=subscriptions_message, headers=headers, timeout=20)
        print(response.json())

        while True:
            event = websocket.recv()
            print(25*"-")
            pprint(json.loads(event))

asyncio.run(listener())
