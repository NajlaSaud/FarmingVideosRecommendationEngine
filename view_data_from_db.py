import pandas as pd
import sqlite3
import openpyxl


conn = sqlite3.connect('farming_video.db')

df = pd.read_sql_query("SELECT * FROM VIDEO ", conn)
print(df)

df = pd.read_sql_query("SELECT * FROM SEARCH ", conn)
print(df)

df = pd.read_sql_query("SELECT * FROM SEARCH_VIDEO ", conn)
print(df)

conn.close()

# conn = sqlite3.connect('video_dataset.db')
# df = pd.read_sql_query("SELECT * FROM VIDEO ", conn)
# print(df)
# df.to_excel('video_dataset_excel.xlsx')
# conn.close()
