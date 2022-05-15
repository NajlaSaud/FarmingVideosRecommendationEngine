import csv
import sqlite3
import urllib.request
import re
import string
import engine
from googleapiclient.discovery import build
import os


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


search_word = 'farming in the desert'
search_keyword = prepare_search_term(search_word)

html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())

conn = sqlite3.connect('farming_video.db')
cursor = conn.cursor()

result = cursor.execute("SELECT video_id FROM VIDEO WHERE video_url_id = '" + video_ids[0] + "'")
print(engine.get_recommendations(result.fetchone()[0]))
