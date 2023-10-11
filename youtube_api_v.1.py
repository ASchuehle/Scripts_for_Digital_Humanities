import os
import googleapiclient.discovery
import pandas as pd
from datetime import datetime

def get_all_video_in_channel(channel_id, output_file):
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "API-Key" # Setzen Sie hier Ihren API-Key ein.

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50, # Das ist die maximale Anzahl von Videos, die pro Anfrage zurückgegeben wird.
        type="video"
    )
    response = request.execute()

    videos = []
    while response:
        for item in response['items']:
            video_id = item['id']['videoId']
            video_title = item['snippet']['title']
            video_url = "https://www.youtube.com/watch?v=" + video_id

            # Hole zusätzliche Daten für dieses Video
            video_request = youtube.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            video_response = video_request.execute()
            video_data = video_response['items'][0]

            # Ändere das Format des Veröffentlichungsdatums
            video_published_at = video_data['snippet']['publishedAt']
            video_published_at = datetime.strptime(video_published_at, "%Y-%m-%dT%H:%M:%SZ")
            video_published_at = video_published_at.strftime("%d.%m.%Y")

            video_likes = video_data['statistics'].get('likeCount', 'N/A')
            video_comments = video_data['statistics'].get('commentCount', 'N/A')
            video_views = video_data['statistics'].get('viewCount', 'N/A')

            videos.append([video_title, video_url, video_published_at, video_likes, video_views, video_comments])

        # Überprüfen, ob es eine nächste Seite gibt
        if 'nextPageToken' in response:
            request = youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,
                type="video",
                pageToken=response['nextPageToken']
            )
            response = request.execute()
        else:
            print("Daten fertig gelesen.")
            break

    # Erstellen Sie einen DataFrame und schreiben Sie ihn in eine Excel-Datei
    df = pd.DataFrame(videos, columns=['title', 'url', 'published_at', 'likes', 'views', 'comments'])
    df.to_excel(output_file, index=False)

current_date = datetime.now().strftime("%d.%m.%Y")

channel_id = input("Bitte geben sie die ID des Kanals ein: ")
output_file = "yt_" + current_date + ".xlsx" #Ändere yt in den Namen des Kanals falls du das Skript mehrfach ausführen möchtest
get_all_video_in_channel(channel_id, output_file)
print("Tabelle " +output_file + " erstellt")