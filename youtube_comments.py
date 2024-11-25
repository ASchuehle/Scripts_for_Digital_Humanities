#!/usr/bin/env python3

import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import re
import html
import pyexcel_ods3
from bs4 import BeautifulSoup

def clean_text(text):
    if isinstance(text, str):
        # Entferne alle nicht-ASCII-Zeichen außer deutschen Umlauten
        text = re.sub(r'[^\x00-\x7FäöüÄÖÜß]+', '', text)
        # HTML-Entities dekodieren (z.B. &quot; -> ")
        text = html.unescape(text)
        # Entferne HTML-Tags (z.B. <b>, <br>, etc.)
        text = BeautifulSoup(text, "html.parser").get_text()
        return text
    return text

def get_replies(youtube, comment_id):
    replies = []
    page_token = None
    while True:
        try:
            reply_request = youtube.comments().list(
                part="snippet",
                parentId=comment_id,
                maxResults=100,
                pageToken=page_token
            )
            reply_response = reply_request.execute()
            for reply in reply_response.get('items', []):
                reply_username = clean_text(reply['snippet']['authorDisplayName'])
                reply_text = clean_text(reply['snippet']['textDisplay'])
                reply_date = reply['snippet']['publishedAt']
                replies.append((reply_username, reply_text, reply_date))
            
            page_token = reply_response.get('nextPageToken')
            if not page_token:
                break
        except HttpError as e:
            print(f"HTTP Error {e.resp.status} while getting replies for comment {comment_id}: {e.content}")
            break
    return replies

def get_comments(youtube, video_id, original_id):
    comments = []
    page_token = None
    while True:
        try:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=100,
                pageToken=page_token,
                textFormat="plainText"
            )
            response = request.execute()

            if 'items' not in response or len(response['items']) == 0:
                print(f"Keine Kommentare für Video {video_id} verfügbar. Möglicherweise sind die Kommentare deaktiviert.")
                break

            for item in response['items']:
                top_comment = item['snippet']['topLevelComment']
                username = clean_text(top_comment['snippet']['authorDisplayName'])
                comment_text = clean_text(top_comment['snippet']['textDisplay'])
                comment_date = top_comment['snippet']['publishedAt']
                comment_id = top_comment['id']
                comments.append((username, original_id, comment_text, comment_date))
                
                # Check if there are more replies to fetch
                total_reply_count = item['snippet']['totalReplyCount']
                if total_reply_count > 0:
                    replies = get_replies(youtube, comment_id)
                    for reply_username, reply_text, reply_date in replies:
                        comments.append((reply_username, original_id, reply_text, reply_date))

            page_token = response.get('nextPageToken')
            if not page_token:
                break

        except HttpError as e:
            if e.resp.status == 403:
                print(f"Kommentare für Video {video_id} sind gesperrt oder nicht zugänglich.")
            else:
                print(f"HTTP Error {e.resp.status} for video {video_id}: {e.content}")
            break
        except KeyError as e:
            print(f"Key error: {str(e)}")
            break

    return comments

def extract_video_ids(url):
    parts = url.split("=")
    return parts[1] if len(parts) > 1 else None

def main(api_key):
    input_file = input("Bitte geben Sie den Dateinamen der ODS-Datei mit den Videos an: ")
    youtube = build('youtube', 'v3', developerKey=api_key)
    data = pd.read_excel(input_file, engine='odf')
    video_urls = data['URL']
    video_ids = data['ID']
    all_comments = []

    for url, original_id in zip(video_urls, video_ids):
        video_id = extract_video_ids(url)
        if video_id:
            comments = get_comments(youtube, video_id, original_id)
            all_comments.extend(comments)

    # Speichere die Kommentare in einer ODS-Datei
    output_file = input_file.replace('.ods', '_comments.ods')
    
    try:
        # Verwende pyexcel_ods3 zum Speichern in ODS-Format
        ods_data = [['Username', 'Original Video ID', 'Comment', 'Date']] + all_comments
        pyexcel_ods3.save_data(output_file, {"Sheet1": ods_data})
        print(f"Datei '{output_file}' wurde erfolgreich erstellt.")
    except Exception as e:
        print(f"Fehler beim Speichern der Datei '{output_file}': {e}")

# Nutze deinen API-Key
API_KEY = 'AIzaSyBLAD5A8tqxnFs430QtJyIazT1dzAXXBfg'

main(API_KEY)
