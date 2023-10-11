import requests
import datetime

def get_video_ids(channel_id, start_date, end_date, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/search"
    video_ids = []

    page_token = None
    while True:
        params = {
            'key': api_key,
            'channelId': channel_id,
            'part': 'id',
            'order': 'date',
            'type': 'video',
            'publishedAfter': start_date.isoformat() + 'Z',
            'publishedBefore': end_date.isoformat() + 'Z',
            'maxResults': 50,  # Max allowed by the API
        }
        
        if page_token:
            params['pageToken'] = page_token
        
        response = requests.get(base_url, params=params).json()
        video_ids += [item['id']['videoId'] for item in response.get('items', [])]

        page_token = response.get('nextPageToken')
        if not page_token:
            break

    return video_ids

def count_comments(video_ids, api_key):
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    total_comments = 0

    for video_id in video_ids:
        params = {
            'key': api_key,
            'id': video_id,
            'part': 'statistics',
        }

        response = requests.get(base_url, params=params).json()
        total_comments += int(response['items'][0]['statistics']['commentCount'])

    return total_comments

def write_to_file(comment_count, start_date, end_date):
    with open("youtube_comments_results.txt", "w") as file:
        file.write(f"Ergebnis vom {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Total comments from {start_date.date()} to {end_date.date()}: {comment_count}\n")
        file.write("\nDiese Analyse wurde von einem Skript ausgeführt aus dem GitHub-Repository:\n")
        file.write("https://github.com/OtterlyAst/CommentCounter\n")

def main():
    API_KEY = 'AIzaSyAcC4QG7BHCDuAb0aW7ZoGed5nIdz2AAX0'
    CHANNEL_ID = 'UC0AXrjhtw-sW2nCGAXEsSrA'
    START_DATE = datetime.datetime(2023, 2, 1)
    END_DATE = datetime.datetime(2023, 7, 31)

    video_ids = get_video_ids(CHANNEL_ID, START_DATE, END_DATE, API_KEY)
    comments_count = count_comments(video_ids, API_KEY)
    write_to_file(comments_count, START_DATE, END_DATE)
    print(f"Ergebnisse wurden in 'youtube_comments_results.txt' geschrieben.")

if __name__ == "__main__":
    main()

