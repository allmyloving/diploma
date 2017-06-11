from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC

from data import db_utils

CLASSIFIERS = {'naive_bayes': MultinomialNB(alpha=0.02),
               'svm': SVC(kernel='linear'),
               'knn': KNeighborsClassifier(n_jobs=-1)}

vectorizer = CountVectorizer(analyzer='char',
                             ngram_range=(1, 3),
                             decode_error='ignore')
transformer = TfidfTransformer(use_idf=False)
clf = None


def train(classifier, data_amount):
    global clf
    __validate_classifier_exists(classifier)
    data = db_utils.retrieve_train_data(data_amount)
    messages = [line[0] for line in data]
    languages = [line[1] for line in data]
    clf = make_pipeline(vectorizer, transformer, CLASSIFIERS[classifier])
    clf.fit(messages, languages)


def predict(message):
    if not clf:
        raise Exception('Classifier should be trained before calling predict')
    return clf.predict([message])[0]


def train_and_evaluate(classifier, data_amount):
    __validate_classifier_exists(classifier)
    train_set = db_utils.retrieve_train_data(data_amount)
    test_set = db_utils.retrieve_test_data(data_amount)
    train_messages = [line[0] for line in train_set]
    train_languages = [line[1] for line in train_set]
    classifier = make_pipeline(vectorizer, transformer, CLASSIFIERS[classifier])
    classifier.fit(train_messages, train_languages)

    test_messages = [line[0] for line in test_set]
    test_languages = [line[1] for line in test_set]
    predicted_languages = classifier.predict(test_messages)

    print(metrics.classification_report(test_languages, predicted_languages))


def __validate_classifier_exists(classifier):
    if not CLASSIFIERS[classifier]:
        raise Exception("Please enter one of the valid classifiers %s" % CLASSIFIERS)
