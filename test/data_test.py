import unittest
import functions


class TestFunctions(unittest.TestCase):
    def test_should_remove_links_and_mentions_from_tweets(self):
        messages = ["I do not like @wikipedia",
                    "Hi I'm learning German https://youtube.com/sdfkj"]
        expected_messages = ["I do not like ",
                             "Hi I'm learning German "]
        self.assertListEqual(functions.remove_redundant_symbols(messages), expected_messages)

    def test_should_remove_tweets_shorter_than_threshold(self):
        messages = ["swarm", "Hi I'm learning German"]
        expected_messages = ["Hi I'm learning German"]
        self.assertListEqual(functions.remove_redundant_symbols(messages), expected_messages)


if __name__ == '__main__':
    unittest.main()
