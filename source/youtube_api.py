"""All functions and features that work with the help of the youtube api"""

import asyncio
from datetime import datetime
import requests
from googleapiclient.discovery import build
import googleapiclient.errors
import db
from generic_functions import MyTemplate
from watcher import logger
from constants import (
    REQUEST_TIMEOUT
)


async def get_latest_yt_videos(
    api_key: str, channel_id: str, max_results: int
) -> list[db.Video]:
    """
    Function fetches the latest videos from youtube and sorts them by the most new.

    Args:
        api_key (str): Youtube API key
        channel_id (str): Channel ID from which the videos are to be fetch
        max_results (int, optional): Number of videos. Defaults to 1.

    Returns:
        list[Video]: List of videos
    """
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        videos: list[db.Video] = []

        response = (
            youtube.search()  # pylint: disable=no-member
            .list(
                part="snippet",
                channelId=channel_id,
                maxResults=max_results,
                order="date",
                type="video",  # No playlists or livestreams
                fields="items(id,snippet(title,publishedAt,channelId))",
            )
            .execute()
        )

        for item in response["items"]:
            if item["snippet"].get("channelId") != channel_id:
                url = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
                channel_id_found = item["snippet"].get("channelId")
                logger.debug(f"Wrong channel id ({channel_id_found}) found with video: {url}")
                continue
            title = item["snippet"]["title"]
            video_id = item["id"]["videoId"]
            published_at = item["snippet"]["publishedAt"]
            url = f'https://www.youtube.com/watch?v={item["id"]["videoId"]}'
            video = db.Video(
                video_id=video_id,
                portal="youtube",
                timestamp=datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ"),
                title=title,
                url=url,
            )
            videos.append(video)
        return videos
    except googleapiclient.errors.HttpError as http_err:
        logger.error(f"YouTube HTTP Error {http_err.resp.status}: {http_err.content}")
        return []
    except OSError as err:
        logger.error(f"Youtube API Error: {err}")
        return []
    except (ValueError, KeyError) as err:
        logger.error(f"API Parameter Error: {err}")
        return []


async def new_yt_video_handler(**settings: dict) -> None:
    """
    Handling function to find new youtube videos and post them

    Args:
        settings (dict): App settings
    """
    logger.debug("Check if new youtube video is available.")
    if not settings["database_synchronized"]:
        await db.sync_db()
        settings["database_synchronized"] = True
    videos = await get_latest_yt_videos(
        settings["youtube_token"],
        settings["youtube_channel_id"],
        settings["yt_max_fetched_videos"],
    )
    if not videos:
        return
    for video in videos:
        if await db.check_video_exist("youtube", video.video_id):
            logger.debug(f"Youtube Video: {video} already exists")
            continue
        logger.info(f"New Youtube video detected: {video.title}")
        _ = await db.add_data(video)
        content = MyTemplate(settings["yt_post_text"]).substitute(
            portal=video.portal, link=video.url
        )
        await post_video(settings, content)
    # await asyncio.sleep(CLIP_WAIT_TIME)


async def post_video(settings: dict, content: str) -> None:
    """Post video in discord with all information

    Args:
        settings (dict): Settings to get access to descord webhook
        content (str): Video link with user information
    """
    data = {"content": content, "username": settings["discord_username_video"]}
    requests.post(settings["webhook_url_video"], data=data, timeout=REQUEST_TIMEOUT)


async def async_main():
    """Scheduling function for regular call."""
    await new_yt_video_handler()


if __name__ == "__main__":
    asyncio.run(async_main())
