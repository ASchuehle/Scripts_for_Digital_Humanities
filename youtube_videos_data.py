#!/usr/bin/env python3

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import isodate  # Importiere das isodate Modul für die ISO 8601 Dauer-Parsing

def get_video_data(video_id, youtube):
    try:
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=video_id
        )
        response = request.execute()

        data = response['items'][0]
        snippet = data['snippet']
        statistics = data['statistics']
        content_details = data['contentDetails']

        publish_date = snippet['publishedAt']
        publish_date = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ").date()

        views = statistics.get('viewCount', 'N/A')
        likes = statistics.get('likeCount', 'N/A')
        comments = statistics.get('commentCount', 'N/A')
        
        # Parse und formatiere die Videolänge in aufgerundeten Minuten
        duration = content_details['duration']
        parsed_duration = isodate.parse_duration(duration)
        total_minutes = (parsed_duration.total_seconds() + 59) // 60  # Runde auf die nächste Minute auf

        return [publish_date, views, likes, comments, int(total_minutes)]
    except HttpError as err:
        print(f"An HTTP error {err.resp.status} occurred: {err.content}")
        return ['Error', 'Error', 'Error', 'Error', 'Error']

def main(api_key, input_file):
    youtube = build('youtube', 'v3', developerKey=api_key)
    df = pd.read_excel(input_file, engine='odf')
    video_ids = df['URL'].apply(lambda x: x.split('=')[1])
    video_data = []

    for video_id in video_ids:
        data = get_video_data(video_id, youtube)
        video_data.append(data)

    results_df = pd.DataFrame(video_data, columns=['Publish Date', 'Views', 'Likes', 'Comments', 'Duration in minutes'])
    results_df.insert(0, 'ID', df['ID'])

    output_file = input_file.replace('.ods', '_data.ods')
    results_df.to_excel(output_file, index=False, engine='odf')
    print(f"Die Tabelle {output_file} wurde erstellt.")

# API Key Abfrage
API_KEY = 'XXX'  # Setze hier deinen API-Schlüssel zwischen die Anführungszeichen

# Abfrage der Quelldatei
INPUT_FILE = input("Bitte geben Sie den Namen der Quelldatei ein (inklusive der Dateiendung, z.B. 'Youtube_Video_List.ods'): ").strip()

main(API_KEY, INPUT_FILE)
