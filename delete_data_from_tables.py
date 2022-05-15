import pandas as pd
import sqlite3

conn = sqlite3.connect('video.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE VIDEO;', )
print('We have deleted', cursor.rowcount, 'records from the table VIDEO.')
conn.commit()

cursor.execute('DROP TABLE SEARCH;', )
print('We have deleted', cursor.rowcount, 'records from the table SEARCH.')
conn.commit()

cursor.execute('DROP TABLE SEARCH_VIDEO;', )
print('We have deleted', cursor.rowcount, 'records from the table SEARCH_VIDEO.')
conn.commit()

conn.close()
