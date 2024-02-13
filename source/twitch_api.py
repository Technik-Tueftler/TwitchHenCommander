"""All functions and features that work with the help of the twitch api
"""

from datetime import datetime, timedelta
import requests
from constants import UPDATE_INTERVAL_PUBLISH_NEW_CLIPS, REQUEST_TIMEOUT
from file_handler import load_last_clip_timestamp


async def fetch_new_clips(settings) -> list:
    """Function to find new clips in the last interval

    Args:
        settings (dict): App settings

    Returns:
        list: List of all clips in last interval
    """
    broadcaster_id = settings["broadcaster_id"]
    client_id = settings["ID"]
    token = settings["token"]
    timestamp = datetime.utcnow()
    # seconds=UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    end_timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    fetch_url = (
        f"https://api.twitch.tv/helix/clips?"
        f"broadcaster_id={broadcaster_id}&"
        f"started_at={start_timestamp}&"
        f"ended_at={end_timestamp}"
    )
    headers = {"Client-ID": client_id, "Authorization": f"Bearer {token}"}
    # {'error': 'Not Found', 'status': 404, 'message': ''}
    response = requests.get(fetch_url, headers=headers, timeout=REQUEST_TIMEOUT).json()
    return response["data"]


async def new_clips_handler(**settings) -> None:
    """Handling function to find new clips and then post them"""
    clips = await fetch_new_clips(settings)
    last_clip_timestamp = await load_last_clip_timestamp()
    # {'data': [], 'pagination': {}}

    # {'data': [
    #   {'id': 'BeautifulAgitatedDunlinOneHand-rJmPn-ITKkDPQH5w',
    #    'url': 'https://clips.twitch.tv/BeautifulAgitatedDunlinOneHand-rJmPn-ITKkDPQH5w',
    #    'embed_url': 'https://clips.twitch.tv/embed?clip=BeautifulAgitatedDunlinOneHand-rJmPn-ITKkDPQH5w',
    #    'broadcaster_id': '206130928',
    #    'broadcaster_name': 'Technik_Tueftler',
    #    'creator_id': '466289382',
    #    'creator_name': 'tim_deutschland',
    #    'video_id': '2052253956',
    #    'game_id': '31339',
    #    'language': 'de',
    #    'title': 'Voller Fokus',
    #    'view_count': 7,
    #    'created_at': '2024-02-03T21:16:52Z',
    #    'thumbnail_url': 'https://clips-media-assets2.twitch.tv/MmRp06yZj5_iEypAz0B-cA/AT-cm%7CMmRp06yZj5_iEypAz0B-cA-preview-480x272.jpg',
    #    'duration': 16, 'vod_offset': 4930, 'is_featured': False}], 'pagination': {}}
    new_clips = [
        clip
        for clip in clips
        if datetime.strptime(clip["created_at"], "%Y-%m-%dT%H:%M:%SZ") > last_clip_timestamp
    ]
    for clip in new_clips:
        # webhook erstellen
        # post
        ...


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
