"""_summary_
"""
import asyncio
from datetime import datetime, timedelta
import requests
from constants import UPDATE_INTERVAL_PUBLISH_NEW_CLIPS, REQUEST_TIMEOUT


async def fetch_new_clips(settings) -> list:
    broadcaster_id = settings["broadcaster_id"]
    client_id = settings["ID"]
    token = settings["token"]
    end_timestamp = (datetime.utcnow()).strftime("%Y-%m-%dT%H:%M:%SZ")
    start_timestamp = (
        end_timestamp - timedelta(seconds=UPDATE_INTERVAL_PUBLISH_NEW_CLIPS)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    fetch_url = f"https://api.twitch.tv/helix/clips?broadcaster_id={broadcaster_id}&started_at={end_timestamp}&ended_at={start_timestamp}"
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    response = requests.get(fetch_url, headers=headers, timeout=REQUEST_TIMEOUT)
    return response["data"]


async def new_clips_handler(**settings) -> None:
    clips = await fetch_new_clips(settings)



def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
