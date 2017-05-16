from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

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


def train_and_evaluate():
    train_set = utils.retrieve_train_data()
    test_set = utils.retrieve_test_data()
    train_messages = [line[0] for line in train_set]
    train_languages = [line[1] for line in train_set]
    clf.fit(train_messages, train_languages)

    test_messages = [line[0] for line in test_set]
    test_languages = [line[1] for line in test_set]
    predicted_languages = clf.predict(test_messages)

    print(metrics.classification_report(test_languages, predicted_languages))
