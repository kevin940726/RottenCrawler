import nltk
import string
import json
import unicodedata
import sys
import numpy as np
from numpy import unravel_index

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer

def remove_punctuation(text):
    return text.translate(dict.fromkeys(i for i in xrange(sys.maxunicode)
        if unicodedata.category(unichr(i)).startswith('P')))

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


def readCritics(movie):
    for critic in movie["critics"]:
        text = critic["review"]
        lowers = text.lower()
        no_punctuation = remove_punctuation(lowers)
        token_dict[movie["movieTitle"]]["critics"].append(no_punctuation)

    # return vect.fit_transform(token_dict[movie["movieTitle"]]["critics"].values())

def readReviews(movie):
    for review in movie["reviews"]:
        text = review["review"]
        lowers = text.lower()
        no_punctuation = remove_punctuation(lowers)
        token_dict[movie["movieTitle"]]["reviews"].append(no_punctuation)

    # return vect.fit_transform(token_dict[movie["movieTitle"]]["reviews"].values())

def addToNewDict(dict, key, value):
    newdict = dict.copy()
    newdict[key] = value
    return newdict


def readMovie(movie):
    token_dict[movie["movieTitle"]] = {"critics": [], "reviews": []}
    readCritics(movie)
    readReviews(movie)

    all_reviews = token_dict[movie["movieTitle"]]["critics"] + token_dict[movie["movieTitle"]]["reviews"]

    tfidf = vect.fit_transform(all_reviews)

    critic_num = len(token_dict[movie["movieTitle"]]["critics"])

    cosine[movie["movieTitle"]] = (tfidf * tfidf.T).A

def recommender(movie):
    avg_cosine = np.average(cosine[movie["movieTitle"]][critic_num:, :critic_num], axis=1)
    sorted_reviewers = np.argsort(avg_cosine)[::-1]
    sorted_reviewers = map(lambda x: addToNewDict(movie["reviews"][x], 'simScore', avg_cosine[x]), sorted_reviewers)
    return sorted_reviewers


def HAC(movie):
    critic_num = len(token_dict[movie["movieTitle"]]["critics"])
    N = len(token_dict[movie["movieTitle"]]["reviews"])
    C = cosine[movie["movieTitle"]][critic_num:, critic_num:]
    I = ~np.identity(N, dtype=bool)
    A = []

    for k in range(0, N-1):
        a = unravel_index(np.where(I, C, -1).argmax(), C.shape)
        A.append((a[0], a[1], C[a[0], a[1]]))

        for j in range(0, N):
            C[a[0], j] = min(C[j, a[0]], C[j, a[1]])
            C[j, a[0]] = min(C[j, a[0]], C[j, a[1]])
            I[a[1],] = False
            I[0:,a[1]] = False

    return A


path = 'rt100Movies.json'
token_dict = {}
stemmer = PorterStemmer()
movieList = {}
cosine = {}
vect = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
reviewer_list = {}
cluster = {}


def main():
    with open(path, 'r') as data_file:
        movieList = json.load(data_file)

    count = 0
    for movie in movieList:
        if movie["reviews"] and movie["critics"]:
            readMovie(movie)
            # reviewer_list[movie["movieTitle"]] = recommender(movie)
            cluster[movie["movieTitle"]] = HAC(movie)

        count += 1
        print count

    with open("clusterList.json", 'w+') as outfile:
        json.dump(cluster, outfile, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    main()
