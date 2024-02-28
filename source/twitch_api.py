"""All functions and features that work with the help of the twitch api
"""

from datetime import datetime, timedelta
from string import Template

import asyncio
import requests
from constants import (
    REQUEST_TIMEOUT,
    UPDATE_INTERVAL_PUBLISH_NEW_CLIPS,
    CLIP_WAIT_TIME,
    DEFAULT_CACHE_DATA,
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
    seconds = UPDATE_INTERVAL_PUBLISH_NEW_CLIPS
    start_timestamp = (timestamp - timedelta(seconds=40)).strftime("%Y-%m-%dT%H:%M:%SZ")
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
    print(last_clip_timestamp)
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
        if datetime.strptime(clip["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        > last_clip_timestamp
    ]
    print(new_clips)
    if not new_clips:
        return
    for clip in new_clips:
        print(clip)
        print(clip["url"])
        print(clip["creator_name"])
        print(settings["clip_thank_you_text"])
        # content_1 = settings["clip_thank_you_text"].format(link=clip["url"], user=clip["creator_name"])
        content = MyTemplate(settings["clip_thank_you_text"]).substitute(
            link=clip["url"], user=clip["creator_name"]
        )
        await post_clips(settings, content)
        await asyncio.sleep(CLIP_WAIT_TIME)
    latest_timestamp = max(
        datetime.strptime(clip["created_at"], TIMESTAMP_PATTERN) for clip in clips
    )

    await save_cache_data(
        {"clip_last_timestamp": latest_timestamp.strftime(TIMESTAMP_PATTERN)}
    )


async def post_clips(settings: dict, content: str) -> None:
    # Clip aus dem aktuellen Stream <Link>. Vielen dank an <Twitch Name>.
    # ToDo: Wollen wir die clip links auch in einem extra File speichern?
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
