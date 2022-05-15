import csv
import sqlite3

conn = sqlite3.connect('farming_video.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM VIDEO")
csv_video_file = open(r"video.csv", 'w', newline='', encoding='UTF8')
with csv_video_file as video_file:
    writer = csv.writer(video_file)
    writer.writerow([i[0] for i in cursor.description])  # Header
    writer.writerows(cursor)

cursor.execute("SELECT * FROM SEARCH_VIDEO")
csv_search_video_file = open(r"search_video.csv", 'w', newline='', encoding='UTF8')
with csv_search_video_file as search_video_file:
    writer = csv.writer(search_video_file)
    writer.writerow([i[0] for i in cursor.description])  # Header
    writer.writerows(cursor)

conn.close()
