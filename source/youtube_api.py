import asyncio
from datetime import datetime
from googleapiclient.discovery import build
import db


async def get_latest_yt_videos(
    api_key: str, channel_id: str, max_results: int = 1
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
    youtube = build("youtube", "v3", developerKey=api_key)

    response = (
        youtube.search()
        .list(
            part="snippet",
            channelId=channel_id,
            maxResults=max_results,
            order="date",
            type="video",  # No playlists or livestreams
        )
        .execute()
    )

    videos = []
    for item in response["items"]:
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


async def new_yt_video_handler(**settings: dict) -> None:
    """
    Handling function to find new youtube videos and post them

    Args:
        settings (dict): App settings
    """
    if not settings["database_synchronized"]:
        await db.sync_db()
        settings["database_synchronized"] = True
    latest_video = (
        await get_latest_yt_videos(
            settings["youtube_token"], settings["youtube_channel_id"]
        )
    )[0]
    latest_stored_video = await db.last_video("youtube")
    if latest_video.video_id == latest_stored_video.video_id:
        return
    _ = await db.add_data(latest_video)


async def async_main():
    """Scheduling function for regular call."""
    await new_yt_video_handler()


if __name__ == "__main__":
    asyncio.run(async_main())
