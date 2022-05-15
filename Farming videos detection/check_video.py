import pickle
import pandas as pd
import sklearn
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split


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

video_title = ['Roblox fast farming']
# load the model from disk
filename = 'trained_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

video_title = vectorizer.transform(video_title)
# print(video_title)
predictions = loaded_model.predict(video_title)
print(predictions)

if predictions == 1:
    print('farming')
else:
    print('not farming')
