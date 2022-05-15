import sqlite3

conn = sqlite3.connect('farming_video.db')
print('Opened database successfully')

conn.execute('''CREATE TABLE SEARCH
          (search_id      INTEGER    PRIMARY KEY   AUTOINCREMENT,
          search_term    TEXT       NOT NULL   UNIQUE);''')
print('Table SEARCH created successfully')
conn.commit()

conn.execute('''CREATE TABLE SEARCH_VIDEO
          (id      INTEGER    PRIMARY KEY   AUTOINCREMENT,
           search_id    INTEGER  NOT NULL,
           video_id     INTEGER  NOT NULL,
           FOREIGN KEY (search_id) REFERENCES SEARCH(search_id),
           FOREIGN KEY (video_id) REFERENCES VIDEO(video_id));''')
print('Table SEARCH_VIDEO created successfully')
conn.commit()


conn.execute('''CREATE TABLE VIDEO
         (video_id      INTEGER    PRIMARY KEY   AUTOINCREMENT,
         video_title    TEXT       NOT NULL,
         video_url_id   CHAR(11)   NOT NULL      UNIQUE);''')
print('Table VIDEO created successfully')
conn.commit()

conn.close()
