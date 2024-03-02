"""
All functions for establishing the connection of a websocket to twitch and catching the callbacks.
"""
import json
import asyncio
from websockets.client import connect
import requests
from constants import TWITCH_WEBSOCKET_URL, TWITCH_SUBSCRIPTION_URL, REQUEST_TIMEOUT
import hashtag_handler as hashh


async def websocket_listener(settings: dict) -> None:
    """Listener function to establishing the connection to twitch api with websocket and
    react to subscriptions

    Args:
        settings (dict): App settings with broadcaster and login information
    """
    async with connect(TWITCH_WEBSOCKET_URL) as websocket:
        welcome_message = json.loads(await websocket.recv())
        websocket_id = welcome_message["payload"]["session"]["id"]
        if settings["start_bot_at_streamstart"]:
            subscriptions_message_online = {
                "type": "stream.online",
                "version": "1",
                "condition": {"broadcaster_user_id": settings["broadcaster_id"]},
                "transport": {"method": "websocket", "session_id": websocket_id},
            }
            headers = {
                "Client-ID": settings["ID"],
                "Authorization": f"Bearer {settings['token']}",
            }
            _ = requests.post(
                TWITCH_SUBSCRIPTION_URL,
                json=subscriptions_message_online,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
        if settings["finish_bot_at_streamend"]:
            subscriptions_message_offline = {
                "type": "stream.offline",
                "version": "1",
                "condition": {"broadcaster_user_id": settings["broadcaster_id"]},
                "transport": {"method": "websocket", "session_id": websocket_id},
            }
            headers = {
                "Client-ID": settings["ID"],
                "Authorization": f"Bearer {settings['token']}",
            }
            _ = requests.post(
                TWITCH_SUBSCRIPTION_URL,
                json=subscriptions_message_offline,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )

        while True:
            event = await websocket.recv()
            event_data = json.loads(event)
            if not "event" in event_data["payload"]:
                continue
            if (
                event_data["payload"]["event"]["broadcaster_user_id"]
                != settings["broadcaster_id"]
            ):
                continue
            if event_data["metadata"]["message_type"] == "notification":
                if event_data["metadata"]["subscription_type"] == "stream.online":
                    await hashh.allow_collecting(True)
                if event_data["metadata"]["subscription_type"] == "stream.offline":
                    await hashh.allow_collecting(False)
                    await hashh.tweet_hashtags()
            await websocket.ping()


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """
    asyncio.run(websocket_listener({}))


if __name__ == "__main__":
    main()
