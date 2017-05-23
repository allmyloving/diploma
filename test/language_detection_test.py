import unittest
import functions
from language_detection import language_detection


class TestLanguageDetection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        functions.load_train_data('en', 50)
        functions.load_train_data('ru', 50)

    def test_should_throw_exception_if_classifier_not_found(self):
        with self.assertRaises(Exception):
            language_detection.train('not_existing_classifier', 200)

    def test_should_throw_exception_if_classifier_is_not_trained(self):
        with self.assertRaises(Exception):
            language_detection.predict(200)

    def test_should_not_throw_exception_if_classifier_is_trained(self):
        language_detection.train('svm', 20)
        self.assertEqual(language_detection.predict('message'), 'en')
        self.assertEqual(language_detection.predict('сообщение'), 'ru')


if __name__ == '__main__':
    unittest.main()
