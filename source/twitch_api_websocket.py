import os
import json
import asyncio
# from pprint import pprint
from websockets.sync.client import connect
import requests
from constants import TWITCH_WEBSOCKET_URL, TWITCH_SUBSCRIPTION_URL, REQUEST_TIMEOUT
import hashtag_handler as hashh

client_id = os.getenv("TW_CLIENT_ID", None)
token = os.getenv("TW_TOKEN", None)


async def websocket_listener(settings: dict) -> None:
    with connect(TWITCH_WEBSOCKET_URL) as websocket:
        welcome_message = json.loads(websocket.recv())
        websocket_id = welcome_message["payload"]["session"]["id"]
        subscriptions_message = {
            "type": "stream.online",
            "version": "1",
            "condition": {"broadcaster_user_id": settings["broadcaster_id"]},
            "transport": {"method": "websocket", "session_id": websocket_id},
        }
        headers = {"Client-ID": settings["ID"], "Authorization": f"Bearer {settings['token']}"}
        response = requests.post(
            TWITCH_SUBSCRIPTION_URL,
            json=subscriptions_message,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        print(response.json())

        while True:
            event = websocket.recv()
            event_data = json.loads(event)
            if event_data["metadata"]["message_type"] == "notification":
                if event_data["payload"]["event"]["broadcaster_user_id"] == settings["broadcaster_id"]:
                    await hashh.allow_collecting(True)
            # print(25 * "-")
            # pprint(json.loads(event))


def main() -> None:
    asyncio.run(websocket_listener({}))

if __name__ == "__main__":
    main()
