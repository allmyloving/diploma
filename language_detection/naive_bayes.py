from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB

from data import utils

clf = Pipeline([
    ('vec', CountVectorizer(analyzer='char', ngram_range=(1, 3))),
    ('tfidf', TfidfTransformer(use_idf=False)),
    ('clf', MultinomialNB())
])


def train():
    data = utils.retrieve_train_data()
    messages = [line[0] for line in data]
    languages = [line[1] for line in data]
    clf.fit(messages, languages)


def predict(message):
    return clf.predict([message])[0]
