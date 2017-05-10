import unittest
import functions


class TestFunctions(unittest.TestCase):
    def test_should_get_correct_amount_of_tweets(self):
        self.assertEqual(len(functions.get_data(100, 'en')), 100)
        self.assertEqual(len(functions.get_data(200, 'en')), 200)

    def test_should_correctly_transform_tweets(self):
        messages = ["I do not like @wikipedia",
                    "Hi I'm learning German https://youtube.com/sdfkj"]
        expected_messages = ["I do not like ",
                             "Hi I'm learning German "]
        self.assertListEqual(functions.remove_redundant_symbols(messages), expected_messages)


if __name__ == '__main__':
    unittest.main()
