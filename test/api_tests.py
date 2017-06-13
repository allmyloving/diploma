import unittest

import requests


class ApiTest(unittest.TestCase):
    server_url = 'http://localhost:5000'

    def setUp(self):
        response = requests.delete('%s/data/' % self.server_url)
        self.assertEqual(response.status_code, 204)

    def test_should_return_ok_for_swagger_page(self):
        response = requests.get('%s/ui' % self.server_url)
        self.assertEqual(response.status_code, 200)

    def test_should_create_and_return_train_data(self):
        response = requests.post('%s/data/train/ru' % self.server_url, json={'amount': '100'})
        self.assertEqual(response.status_code, 201)

        response = requests.get('%s/data/train/ru' % self.server_url)
        self.assertEqual(response.status_code, 200)

        response = response.json()
        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 100)

    def test_should_create_and_return_test_data(self):
        response = requests.post('%s/data/test/ru' % self.server_url, json={'amount': '100'})
        self.assertEqual(response.status_code, 201)

        response = requests.get('%s/data/test/ru' % self.server_url)
        self.assertEqual(response.status_code, 200)

        response = response.json()
        self.assertTrue(isinstance(response, list))
        self.assertEqual(len(response), 100)

    def test_should_throw_400_if_amount_is_missing(self):
        response = requests.post('%s/data/train/ru' % self.server_url)
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_should_throw_400_if_amount_is_not_a_number(self):
        response = requests.post('%s/data/train/ru' % self.server_url, json={'amount': 'nan'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_detect_language_should_throw_400_if_text_is_missing(self):
        response = requests.post('%s/lang/detect' % self.server_url, json={'classifier': 'svm'})
        self.assertEqual(response.status_code, 400)
        self.assertTrue('error' in response.json())

    def test_should_return_404_json_when_page_do_not_exist(self):
        response = requests.get('%s/notfound' % self.server_url)
        self.assertEqual(response.status_code, 404)
        self.assertTrue('error' in response.json())


if __name__ == '__main__':
    unittest.main()
