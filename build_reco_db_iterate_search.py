import csv
import urllib.request
import string
from googleapiclient.discovery import build
import sqlite3
import pickle
import pandas as pd
import sklearn
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Get API key
API_KEY = 'AIzaSyDh8g550F3L5Hi4-pcVYAp6IyjkjPoEKO4'

# Build YouTube variable
youtube = build('youtube', 'v3', developerKey=API_KEY)

# Create connection to video database
conn = sqlite3.connect('farming_video.db')
print('Database Opened Successfully')


# Removes punctuation and special characters
def clean_text(df, text_field, new_text_field_name):
    df[new_text_field_name] = df[text_field].str.lower()
    df[new_text_field_name] = df[new_text_field_name].apply(
        lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem))
    # remove numbers
    df[new_text_field_name] = df[new_text_field_name].apply(lambda elem: re.sub(r"\d+", "", elem))

    return df


pd.set_option('display.max_colwidth', -1)
# nltk.download('stopwords')

stop = stopwords.words('english')
# Reads in the data
file_name = 'video_dataset (2).csv'
train_data = pd.read_csv(file_name)
# Drops all columns text and target
cols_to_drop = ['video_url_id']
train_data = train_data.drop(cols_to_drop, axis=1)

data_clean = clean_text(train_data, 'video_title', 'video_title')
# Removes stop words
data_clean['video_title'] = data_clean['video_title'].apply(
    lambda x: ' '.join([word for word in x.split() if word not in stop]))

X_train, X_test, y_train, y_test = train_test_split(data_clean['video_title'], data_clean['label'], random_state=0)

vectorizer = TfidfVectorizer(min_df=10)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

filename = 'trained_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))


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
        # break_flag = False
        for video in data['items']:
            # Check title: if it is not farming: ignore this title (continue)
            title = video['snippet']['title']
            vectorized_title = [title]
            vectorized_title = vectorizer.transform(vectorized_title)
            prediction = loaded_model.predict(vectorized_title)
            if prediction == 1:
                titles_list.append(title)
                # break_flag = True
                # break
                # print('not farming video')
                # continue
            # if break_flag:
            #     continue

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


search_word = 'fast farming'
search_keyword = prepare_search_term(search_word)

# Insert search term into SEARCH table
try:
    conn.execute("INSERT INTO SEARCH(search_term) VALUES('" + search_word + "');")
    print('The search term: ' + search_word + ' is added Successfully')
    conn.commit()
except Exception as e:
    print(e)
    print("search term " + search_word + "has been added before")

# Perform a YouTube search with the search word
video_ids = search_youtube(prepare_search_term(search_word))

# Insert videos into VIDEO table
# Records or rows in a list
# records = []
# for i in range(len(video_ids)):
#     request = youtube.videos().list(
#         part="snippet",
#         id=video_ids[i]
#     )
#     data = request.execute()
#     for video in data['items']:
#         title = video['snippet']['title']
#     records.append((title, video_ids[i]))

cursor = conn.cursor()

# insert multiple records
for i in range(len(video_ids)):
    request = youtube.videos().list(
        part="snippet",
        id=video_ids[i]
    )
    data = request.execute()

    for video in data['items']:
        # Check title: if it is not farming: ignore this title (continue)
        title = video['snippet']['title']
        vectorized_title = [title]
        vectorized_title = vectorizer.transform(vectorized_title)
        prediction = loaded_model.predict(vectorized_title)
        if prediction == 1:
            try:
                conn.execute("INSERT INTO VIDEO(video_title,video_url_id) VALUES('" + title + "', '" + video_ids[i] + "');")
                conn.commit()
            except BaseException as e:
                print(e)
                print("video " + video_ids[i] + "has been added before")
                continue

conn.execute("INSERT INTO SEARCH_VIDEO(search_id, video_id) "
             "SELECT SEARCH.search_id, VIDEO.video_id "
             "FROM SEARCH, VIDEO "
             "WHERE (SEARCH.search_term = '" + search_word + "');")
conn.commit()

titles = extract_video_titles(video_ids)
keywords = []
for i in range(0, 2):
    if i > 0:
        titles = new_titles
    for title in titles:
        # Insert title into SEARCH table
        # keywords.append(prepare_search_term(title))
        try:
            conn.execute("INSERT INTO SEARCH(search_term) VALUES('" + title + "');")
            print('The search term: ' + title + ' is added Successfully')
            conn.commit()
        except Exception as e:
            print(e)
            print("search term " + title + "has been added before")
            continue

        # Perform a YouTube search with the title
        video_ids = search_youtube(prepare_search_term(title))
        try:
            new_titles = extract_video_titles(video_ids)
        except Exception as e:
            print(e)
            continue

        cursor = conn.cursor()

        # insert multiple records
        for i in range(len(video_ids)):
            request = youtube.videos().list(
                part="snippet",
                id=video_ids[i]
            )
            data = request.execute()
            for video in data['items']:
                title = video['snippet']['title']
                vectorized_title = [title]
                vectorized_title = vectorizer.transform(vectorized_title)
                prediction = loaded_model.predict(vectorized_title)
                if prediction == 1:
                    try:
                        conn.execute(
                            "INSERT INTO VIDEO(video_title,video_url_id) VALUES('" + title + "', '" + video_ids[i] + "');")
                        conn.commit()
                    except BaseException as e:
                        print(e)
                        print("video " + video_ids[i] + "has been added before")
                        continue

        conn.execute("INSERT INTO SEARCH_VIDEO(search_id, video_id) "
                     "SELECT SEARCH.search_id, VIDEO.video_id "
                     "FROM SEARCH, VIDEO "
                     "WHERE (SEARCH.search_term = '" + search_word + "');")
        conn.commit()

conn.close()
