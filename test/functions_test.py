import unittest
from functions import *


class TestFunctions(unittest.TestCase):
    def setUp(self):
        cleanup_all_data()

    def test_should_remove_links_and_mentions_from_tweets(self):
        messages = ["I do not like @wikipedia",
                    "Hi I'm learning German https://youtube.com/sdfkj"]
        expected_messages = ["I do not like ",
                             "Hi I'm learning German "]
        self.assertListEqual(remove_redundant_symbols(messages), expected_messages)

    def test_should_remove_tweets_shorter_than_threshold(self):
        messages = ["swarm", "Hi I'm learning German"]
        expected_messages = ["Hi I'm learning German"]
        self.assertListEqual(remove_redundant_symbols(messages), expected_messages)

    def test_should_raise_exception_when_call_load_test_data_consequently(self):
        load_test_data('en', 100)
        with self.assertRaises(Exception):
            load_test_data('en', 100)

    def test_should_raise_exception_when_call_load_train_data_consequently(self):
        load_train_data('en', 100)
        with self.assertRaises(Exception):
            load_train_data('en', 100)

    def test_should_load_correct_amount_of_train_data(self):
        load_train_data('en', 200)
        self.assertEqual(200, TestFunctions.get_train_data_amount('en'))

    def test_should_load_correct_amount_of_test_data(self):
        load_test_data('en', 200)
        self.assertEqual(200, TestFunctions.get_test_data_amount('en'))

    @staticmethod
    def get_test_data_amount(lang):
        return len(retrieve_test_data(lang))

    @staticmethod
    def get_train_data_amount(lang):
        return len(retrieve_train_data(lang))


if __name__ == '__main__':
    unittest.main()
