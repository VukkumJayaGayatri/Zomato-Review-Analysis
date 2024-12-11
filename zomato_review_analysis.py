# -*- coding: utf-8 -*-
"""Zomato Review Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11y5QR_BvOOuHQTbn_q7MhdjSjvzaOSra
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the dataset with error handling
dataset = pd.read_csv('/content/Zomato Review Kaggle.csv', delimiter=',', quoting=3, encoding='latin-1', on_bad_lines='skip')

# Inspect the first few rows
print(dataset.head())
print(dataset.columns)

"""Cleaning the Dataset"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []

print(dataset.columns)

# Filter out non-string reviews
dataset = dataset[dataset['Review'].apply(lambda x: isinstance(x, str))]

# Process the reviews
for i in range(len(dataset)):
    zomato_ratings = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    zomato_ratings = zomato_ratings.lower().split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    zomato_reviews = [ps.stem(word) for word in zomato_ratings if word not in set(all_stopwords)]
    corpus.append(' '.join(zomato_reviews))

print(corpus)

# Clear the corpus list if already used
corpus = []

# Filter out non-string reviews
dataset = dataset[dataset['Review'].apply(lambda x: isinstance(x, str))]

# Process the reviews
for i in range(len(dataset)):
    zomato_ratings = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    zomato_ratings = zomato_ratings.lower().split()
    ps = PorterStemmer()
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not')
    zomato_reviews = [ps.stem(word) for word in zomato_ratings if word not in set(all_stopwords)]

    # Append as a single string
    corpus.append(' '.join(zomato_reviews))

print(corpus)

"""Bag of Words Creation"""

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1600)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, -1].values

"""Splitting Data into test and train dataset

"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 21)

"""Training Naive Bayes"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

"""Predicting on test dataset"""

y_pred=classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

"""Making Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)
