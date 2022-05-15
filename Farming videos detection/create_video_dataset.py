import csv
import urllib.request
import re
import string
from googleapiclient.discovery import build
import sqlite3
import pandas as pd

conn = sqlite3.connect('video_dataset.db')
print('Opened database successfully')

# conn.execute('''CREATE TABLE VIDEO
#          (video_id      INTEGER    PRIMARY KEY   AUTOINCREMENT,
#          video_title    TEXT       NOT NULL,
#          video_tags     TEXT,
#          video_url_id   CHAR(11)   NOT NULL      UNIQUE);''')
# print('Table VIDEO created successfully')
# conn.commit()

# Get API key
API_KEY = 'AIzaSyDh8g550F3L5Hi4-pcVYAp6IyjkjPoEKO4'

# Build YouTube variable
youtube = build('youtube', 'v3', developerKey=API_KEY)


# returns a string that can be used in a youtube search
def prepare_search_term(search_keyword):
    search_term = search_keyword
    # Clean the text

    # Punctuations
    punct = set(string.punctuation)
    punct.add('✔')
    search_term = "".join([ch for ch in search_term if ch not in punct])
    # Remove unicode text
    search_term = search_term.encode(encoding="ascii", errors="ignore").decode()

    # Split the text
    search_term = search_term.split()

    # Join with '+'
    search_term = '+'.join(search_term)

    # return search term
    return search_term


# returns a list of titles
def extract_video_titles(video_ids):
    # Get title for each YouTube video
    titles_list = []
    for i in range(0, len(video_ids)):
        request = youtube.videos().list(
            part="snippet",
            id=video_ids[i]
        )
        data = request.execute()
        for video in data['items']:
            title = video['snippet']['title']
            titles_list.append(title)

    # Return title
    return titles_list


# return a list of video ids
def search_youtube(search_term):
    # Search Youtube videos
    import urllib.request
    import re

    # search_keyword
    search_keyword = search_term

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

    # search results
    return video_ids


search_word = 'Modern Farming Machines'
search_keyword = prepare_search_term(search_word)


# Perform a YouTube search with the search word
video_ids = search_youtube(prepare_search_term(search_word))

cursor = conn.cursor()

# insert multiple records
for i in range(len(video_ids)):
    # try:
    #     title = 'just for try'
    #     conn.execute("INSERT INTO VIDEO(video_title, video_url_id) VALUES('" + title + "', '" + video_ids[i] + "');")
    # except BaseException as e:
    #     print(e)
    #     # print("video " + video_ids[i] + "has been added before")
    #     continue
    request = youtube.videos().list(
        part="snippet",
        id=video_ids[i]
    )
    data = request.execute()
    for video in data['items']:
        tags = video['snippet'].get('tags', 0)
        # Convert tags into one string
        if isinstance(tags, list):
            tags = ' '.join(tags)
        if isinstance(tags, int):
            tags = str(tags)
        title = video['snippet']['title']
    try:
        conn.execute("INSERT INTO VIDEO(video_title,video_tags, video_url_id) VALUES('" + title + "', '" + tags + "', '" + video_ids[i] + "');")
        conn.commit()
        print('Video added successfully')
    except BaseException as e:
        print(e)
        # print("video " + video_ids[i] + "has been added before")
        continue


titles = extract_video_titles(video_ids)
keywords = []
for i in range(0, 4):
    if i > 0:
        titles = new_titles
    for title in titles:
        # Perform a YouTube search with the title
        video_ids = search_youtube(prepare_search_term(title))
        try:
            new_titles = extract_video_titles(video_ids)
        except Exception as e:
            print(e)
            continue

        # Insert videos into VIDEO table
        cursor = conn.cursor()

        # insert multiple records
        for i in range(len(video_ids)):
            # try:
            #     title = 'just for try'
            #     conn.execute(
            #         "INSERT INTO VIDEO(video_title, video_url_id) VALUES('" + title + "', '" + video_ids[i] + "');")
            # except BaseException as e:
            #     print(e)
            #     # print("video " + video_ids[i] + "has been added before")
            #     continue
            request = youtube.videos().list(
                part="snippet",
                id=video_ids[i]
            )
            data = request.execute()
            for video in data['items']:
                tags = video['snippet'].get('tags', 0)
                # Convert tags into one string
                if isinstance(tags, list):
                    tags = ' '.join(tags)
                if isinstance(tags, int):
                    tags = str(tags)
                title = video['snippet']['title']
            try:
                conn.execute(
                    "INSERT INTO VIDEO(video_title,video_tags,video_url_id) VALUES('" + title + "', '" + tags + "', '" + video_ids[i] + "');")
                conn.commit()
                print('Video added successfully')
            except BaseException as e:
                print(e)
                # print("video " + video_ids[i] + "has been added before")
                continue

df = pd.read_sql_query("SELECT * FROM VIDEO ", conn)
print(df)
conn.close()

