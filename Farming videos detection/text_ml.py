import matplotlib
import pandas as pd
import re
import nltk.corpus
from matplotlib import pyplot
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from shap import maskers
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from yellowbrick.text import FreqDistVisualizer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
import sklearn
import shap
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import pickle
# import eli5

pd.set_option('display.max_colwidth', -1)
# nltk.download('stopwords')

stop = stopwords.words('english')
# Reads in the data
# train_data = pd.read_csv('train.csv')
video_data_xlsx = pd.read_excel('video_ dataset.xlsx')
file_name = 'video_dataset.csv'
video_data_xlsx.to_csv(file_name, encoding='utf-8', index=False)
train_data = pd.read_csv(file_name)
# Drops all columns text and target
# cols_to_drop = ['id', 'keyword', 'location']
cols_to_drop = ['video_url_id']
train_data = train_data.drop(cols_to_drop, axis=1)


# Removes punctuation and special characters
def clean_text(df, text_field, new_text_field_name):
    df[new_text_field_name] = df[text_field].str.lower()
    df[new_text_field_name] = df[new_text_field_name].apply(
        lambda elem: re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", elem))
    # remove numbers
    df[new_text_field_name] = df[new_text_field_name].apply(lambda elem: re.sub(r"\d+", "", elem))

    return df


data_clean = clean_text(train_data, 'video_title', 'video_title')
data_clean = clean_text(train_data, 'video_tags', 'video_tags')
# Removes stop words
data_clean['video_title'] = data_clean['video_title'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))
data_clean['video_tags'] = data_clean['video_tags'].apply(lambda x: ' '.join([word for word in x.split() if word not in stop]))

vectorizer = CountVectorizer()
docs = vectorizer.fit_transform(data_clean['video_title'])
features = vectorizer.get_feature_names_out()
visualizer = FreqDistVisualizer(features=features, orient='v')
visualizer.fit(docs)
visualizer.show()

farming_videos = data_clean[data_clean['label'] == 1]
print(farming_videos)
vectorizer = CountVectorizer()
docs = vectorizer.fit_transform(farming_videos['video_title'])
features_farming = vectorizer.get_feature_names_out()
visualizer_farming = FreqDistVisualizer(features=features_farming, orient='v')
visualizer_farming.fit(docs)
visualizer_farming.show()

not_farming_videos = data_clean[data_clean['label'] == 0]
vectorizer = CountVectorizer()
docs = vectorizer.fit_transform(not_farming_videos['video_title'])
features_not_farming = vectorizer.get_feature_names_out()
visualizer_not_farming = FreqDistVisualizer(features=features_not_farming, orient='v')
visualizer_not_farming.fit(docs)
visualizer_not_farming.show()

X_train, X_test, y_train, y_test = train_test_split(data_clean['video_title'], data_clean['label'], random_state=0)
# print(X_train)
# print(y_train)
vectorizer = TfidfVectorizer(min_df=10)
X_train = vectorizer.fit_transform(X_train)
filename = 'trained_vectorizer.sav'
pickle.dump(vectorizer, open(filename, 'wb'))
X_test = vectorizer.transform(X_test)
# model = LogisticRegression(penalty="l2", C=0.1)
# model.fit(X_train, y_train)
model = LogisticRegression()
kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
print(cv_results)
model.fit(X_train, y_train)
# # Spot Check Algorithms
# models = [('LR', LogisticRegression(solver='liblinear', multi_class='ovr')), ('LDA', LinearDiscriminantAnalysis()),
#           ('KNN', KNeighborsClassifier()), ('CART', DecisionTreeClassifier()), ('NB', GaussianNB()),
#           ('SVM', SVC(gamma='auto'))]
# # evaluate each model in turn
# results = []
# names = []
# for name, model in models:
#     kfold = StratifiedKFold(n_splits=10, random_state=1, shuffle=True)
#     cv_results = cross_val_score(model, X_train, y_train, cv=kfold, scoring='accuracy')
#     results.append(cv_results)
#     names.append(name)
#     print('%s: %f (%f)' % (name, cv_results.mean(), cv_results.std()))
#
# # Compare Algorithms
# pyplot.boxplot(results, labels=names)
# pyplot.title('Algorithm Comparison')
# pyplot.show()

# shap.initjs()
# explainer = shap.LinearExplainer(model, X_train, maskers.Independent)
# shap_values = explainer.shap_values(X_test)
# X_test_array = X_test.toarray()
# shap.summary_plot(shap_values, X_test_array, feature_names=vectorizer.get_feature_names_out())
#
# ind = 0
# shap.force_plot(
#     explainer.expected_value, shap_values[ind,:], X_test_array[ind,:],
#     feature_names=vectorizer.get_feature_names_out()
# )


# eli5.show_weights(model, vec=vectorizer, top=10)
print(model)
predictions = model.predict(X_test)
# print(predictions)

# Evaluate predictions
print(accuracy_score(y_test, predictions))
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions))


# save the model to disk
filename = 'trained_model.sav'
pickle.dump(model, open(filename, 'wb'))


# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)
print(X_test)
predictions = loaded_model.predict(X_test)
print(predictions)
