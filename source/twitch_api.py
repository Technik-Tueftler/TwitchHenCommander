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
    timestamp = datetime.utcnow()
    # seconds=UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (
        timestamp - timedelta(days=2)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    fetch_url = (
        f"https://api.twitch.tv/helix/clips?"
        f"broadcaster_id={broadcaster_id}&"
        f"started_at={start_timestamp}&"
        f"ended_at={end_timestamp}"
    )
    print(fetch_url)
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    # {'error': 'Not Found', 'status': 404, 'message': ''}
    response = requests.get(fetch_url, headers=headers, timeout=REQUEST_TIMEOUT).json()
    return response


async def new_clips_handler(**settings) -> None:
    clips = await fetch_new_clips(settings)
    print(clips)



def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
