"""All functions and features that work with the help of the twitch api
"""

from datetime import datetime, timedelta
from string import Template

import asyncio
import requests
import db
from constants import (
    REQUEST_TIMEOUT,
    UPDATE_INTERVAL_PUBLISH_NEW_CLIPS,
    CLIP_WAIT_TIME,
    TIMESTAMP_PATTERN,
)
from file_handler import load_last_clip_timestamp, save_cache_data


class MyTemplate(Template):
    delimiter = "#"


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
    seconds = 40 # UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")
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
    last_clip_ids = await db.fetch_last_clip_ids() # ["clip_id_1, clip_id_2, clip_id_3"]
    # print(last_clip_timestamp)
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
        if clip["id"] in last_clip_ids
    ]
    print(new_clips)
    if not new_clips:
        return
    for clip in new_clips:
        # Step 1
            # Prüfe ob creator_id des clip schon existiert
                # Ja -> fetch User mit twitch_user_id, commit new Clip mit user.id
                # Nein -> create User und commit Clip
        # Step 2
            # Post clip

        content = MyTemplate(settings["clip_thank_you_text"]).substitute(
            link=clip["url"], user=clip["creator_name"]
        )
        await post_clips(settings, content)
        await asyncio.sleep(CLIP_WAIT_TIME)


async def post_clips(settings: dict, content: str) -> None:
    """Post clip in discord with all information

    Args:
        settings (dict): Settings to get access to descord webhook
        content (str): Clip link with user information
    """
    if not settings["dc_feature_clips"]:
        return
    data = {"content": content, "username": settings["discord_username_clip"]}
    requests.post(settings["webhook_url_clip"], data=data, timeout=REQUEST_TIMEOUT)


def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()
