import wsgi
import unittest
from app.request_error import RequestError
import random
from werkzeug.exceptions import HTTPException


class AppTestCase(unittest.TestCase):

    def setUp(self):
        wsgi.app.config['TESTING'] = True
        self.app = wsgi.app.test_client()

    def tearDown(self):
        pass

    def test_search(self):
        rv = self.app.post('/v1/view/searchByWords')
        assert b'Not Implemented' in rv.data

    def test_get_full_tag_list(self):
        rv = self.app.get('/v1/view/getFullTagList')
        assert b'Not Implemented' in rv.data


if __name__ == '__main__':
    unittest.main()
