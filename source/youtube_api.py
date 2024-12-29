import asyncio
from datetime import datetime
from collections import namedtuple
from googleapiclient.discovery import build

Video = namedtuple("Video", ["title", "video_id", "published_at", "url"])

# API-Schlüssel hier einfügen
API_KEY = "AIzaSyCfe8Lb8CKG1y03M8K3HaTzYvRHw6jKIKQ"
CHANNEL_ID = "UCehPIrjonwcDm2gNyWws1Jw"

async def get_latest_videos(api_key: str, channel_id: str, max_results:int = 1) -> list[Video]:
    """
    Function fetches the latest videos from youtube and sorts them by the most new.

    Args:
        api_key (str): Youtube API key
        channel_id (str): Channel ID from which the videos are to be fetch
        max_results (int, optional): Number of videos. Defaults to 1.

    Returns:
        list[Video]: List of videos
    """
    youtube = build("youtube", "v3", developerKey=api_key)

    response = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=max_results,
        order="date",
        type="video"   # No playlists or livestreams
    ).execute()

    videos = []
    for item in response["items"]:
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        published_at = item["snippet"]["publishedAt"]
        url = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
        video = Video(title=title, video_id=video_id, published_at=published_at, url=url)
        videos.append(video)
    return videos


async def new_yt_video_handler(**settings: dict) -> None:
    """
    Handling function to find new youtube videos and post them
    
    Args:
        settings (dict): App settings
    """
    latest_video = (await get_latest_videos(API_KEY, CHANNEL_ID))[0]
    print(latest_video.title)
    date_object = datetime.strptime(latest_video.published_at, "%Y-%m-%dT%H:%M:%SZ")
    print(date_object)
    print(type(date_object))


async def async_main():
    await new_yt_video_handler()


if __name__ == "__main__":
    asyncio.run(async_main())
