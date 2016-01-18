import requests
import json
import numpy as np
import nltk
import nltk.classify.util
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

path = 'rt100Movies.json'
movieList = {}
all_reviews = []
new_review = {}
word_features = []


def sentiment(movie):
    for review in movie['reviews']:
        r = requests.post("http://text-processing.com/api/sentiment/", data={'text': review['review']})
        review.update({'sentiment': r.text})

    return movie['reviews']

def getAllReviews(movieList):
    reviews = np.array(map(lambda x: x["reviews"] or [], movieList))
    reviews = np.concatenate(reviews)

    tokenizeReview = []

    for review in reviews:
        s = review['review']
        s = RegexpTokenizer(r'\w+').tokenize(s.lower())
        s = map(lambda x: PorterStemmer().stem(x), s)
        s = filter(lambda x: x not in stopwords.words('english'), s)
        tokenizeReview.append((s, 'pos' if review["score"] >= 30 else 'neg'))

    return tokenizeReview

def getAllCritics(movieList):
    reviews = np.array(map(lambda x: x["critics"] or [], movieList))
    reviews = np.concatenate(reviews)

    tokenizeReview = []

    for review in reviews:
        s = review['review']
        s = RegexpTokenizer(r'\w+').tokenize(s.lower())
        s = map(lambda x: PorterStemmer().stem(x), s)
        s = filter(lambda x: x not in stopwords.words('english'), s)
        tokenizeReview.append((s, 'pos' if review["tomatometer"] == "fresh" else 'neg'))

    return tokenizeReview

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


def main():
    with open(path, 'r') as data_file:
        movieList = json.load(data_file)

    all_reviews = getAllReviews(movieList)
    word_features = get_word_features(get_words_in_tweets(all_reviews))

    training_set = [({word: (word in x[0]) for word in word_features}, x[1]) for x in all_reviews]
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    all_critics = getAllCritics(movieList)
    testing_set = [({word: (word in x[0]) for word in word_features}, x[1]) for x in all_critics]
    most_informative = classifier.show_most_informative_features(100)
    accuracy = nltk.classify.util.accuracy(classifier, testing_set)
    print accuracy

    with open("most_informative.txt", 'w+') as outfile:
        outfile.write(most_informative)

if __name__ == "__main__":
    main()
