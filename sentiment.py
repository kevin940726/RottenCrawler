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
    reviews = np.array(map(lambda x: x["reviews"], movieList))
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
    reviews = np.array(map(lambda x: x["critics"], movieList))
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


def save_most_informative_features(self, n=10):
    strlist = []
    # Determine the most relevant features, and display them.
    cpdist = self._feature_probdist
    strlist.append('Most Informative Features')

    for (fname, fval) in self.most_informative_features(n):
        def labelprob(l):
            return cpdist[l, fname].prob(fval)

        labels = sorted([l for l in self._labels
                         if fval in cpdist[l, fname].samples()],
                        key=labelprob)
        if len(labels) == 1:
            continue
        l0 = labels[0]
        l1 = labels[-1]
        if cpdist[l0, fname].prob(fval) == 0:
            ratio = 'INF'
        else:
            ratio = '%8.1f' % (cpdist[l1, fname].prob(fval) /
                               cpdist[l0, fname].prob(fval))
        strlist.append(('%24s = %-14r %6s : %-6s = %s : 1.0' %
               (fname, fval, ("%s" % l1)[:6], ("%s" % l0)[:6], ratio)))

    return strlist

def main():
    with open(path, 'r') as data_file:
        movieList = json.load(data_file)

    all_reviews = getAllReviews(movieList[0:50])
    word_features = get_word_features(get_words_in_tweets(all_reviews))

    training_set = [({word: (word in x[0]) for word in word_features}, x[1]) for x in all_reviews]
    classifier = nltk.NaiveBayesClassifier.train(training_set)

    all_critics = getAllCritics(movieList)
    testing_set = [({word: (word in x[0]) for word in word_features}, x[1]) for x in all_critics]
    most_informative = save_most_informative_features(classifier, len(word_features))
    accuracy = nltk.classify.util.accuracy(classifier, testing_set)
    print accuracy

    with open("most_informative_rc.txt", 'w+') as outfile:
        outfile.write("%f\n" % accuracy)
        for feature in most_informative:
            outfile.write("%s\n" % feature)

if __name__ == "__main__":
    main()
