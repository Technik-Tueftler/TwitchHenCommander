from googleapiclient.discovery import build

# API-Schlüssel hier einfügen
API_KEY = 'DEIN_API_SCHLÜSSEL'
CHANNEL_ID = 'DEIN_CHANNEL_ID'

def get_latest_videos(api_key, channel_id, max_results=5):
    # YouTube API-Client initialisieren
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Kanalinformationen abrufen
    response = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        maxResults=max_results,
        order='date',  # Neueste Videos zuerst
        type='video'   # Nur Videos, keine Playlists oder Livestreams
    ).execute()
    
    videos = []
    for item in response['items']:
        video_data = {
            'title': item['snippet']['title'],
            'videoId': item['id']['videoId'],
            'publishedAt': item['snippet']['publishedAt'],
            'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        }
        videos.append(video_data)
    
    return videos

# Neueste Videos abrufen
latest_videos = get_latest_videos(API_KEY, CHANNEL_ID)

# Ergebnisse ausgeben
for video in latest_videos:
    print(f"Title: {video['title']}")
    print(f"Published At: {video['publishedAt']}")
    print(f"URL: {video['url']}\n")


async def new_yt_video_handler(**settings) -> None:

    #if not settings["database_synchronized"]:

def main() -> None:
    """
    Scheduling function for regular call.
    :return: None
    """


if __name__ == "__main__":
    main()