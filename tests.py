# coding=utf-8
import sys
sys.path.insert(1, 'google_appengine')
sys.path.insert(1, 'google_appengine/lib/yaml/lib')
sys.path.insert(1, './lib')


# @kesor's URLFetch Mock: https://gist.github.com/kesor/1179782
from google.appengine.api import apiproxy_stub
from google.appengine.api import apiproxy_stub_map
class FetchServiceMock(apiproxy_stub.APIProxyStub):
    def __init__(self, service_name='urlfetch'):
        super(FetchServiceMock, self).__init__(service_name)

    def set_return_values(self, **kwargs):
        self.return_values = kwargs

    def _Dynamic_Fetch(self, request, response):
        rv = self.return_values
        response.set_content(rv.get('content', ''))
        response.set_statuscode(rv.get('status_code', 500))
        for header_key, header_value in rv.get('headers', {}):
            new_header = response.add_header() # prototype for a header
            new_header.set_key(header_key)
            new_header.set_value(header_value)
        response.set_finalurl(rv.get('final_url', request.url))
        response.set_contentwastruncated(rv.get('content_was_truncated', False))

        # allow to query the object after it is used
        self.request = request
        self.response = response
urlfetch_mock = FetchServiceMock()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', urlfetch_mock)
urlfetch_mock.set_return_values(content='some content')
# end @kesor's Mock


from unittest import TestCase
import webapp2
from webapp2_extras import json
from main import app


class TestApp(TestCase):
    def test_show_error(self):
        request = webapp2.Request.blank("/")
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertDictEqual(
                json.decode(response.body),
                {"name": "I am Spell bot (https://telegram.me/spell_bot)",
                 "result": "Info"})

    def test_get(self):
        request = webapp2.Request.blank("/")
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertDictEqual(
                json.decode(response.body),
                {"name": "I am Spell bot (https://telegram.me/spell_bot)",
                 "result": "Info"})

    def test_bad_post(self):
        request = webapp2.Request.blank("/")
        request.method = "POST"
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertDictEqual(
                json.decode(response.body),
                {"name": "I am Spell bot (https://telegram.me/spell_bot)",
                 "result": "Info"})

    def test_json_empty_post(self):
        request = webapp2.Request.blank("/")
        request.method = "POST"
        request.headers["Content-Type"] = "application/json"
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertDictEqual(
                json.decode(response.body),
                {"name": "I am Spell bot (https://telegram.me/spell_bot)",
                 "result": "Info"})

    def test_json_start_post(self):
        request = webapp2.Request.blank("/")
        request.method = "POST"
        request.headers["Content-Type"] = "application/json"
        request.body = json.encode({
            'update': 1,
            'message': {
                u'date': 1450696897,
                u'text': u'/start',
                u'from': {
                    u'username': u'm_messiah',
                    u'first_name': u'Maxim',
                    u'last_name': u'Muzafarov',
                    u'id': 3798371
                },
                u'message_id': 1,
                u'chat': {
                    u'type': u'group',
                    u'id': -11812986,
                    u'title': u'КС'
                }
            }
        })
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertDictEqual(
                json.decode(response.body),
                {
                    'method': 'sendMessage',
                    'text': u"Привет! Я буду исправлять твои "
                            u"ошибки в режиме inline",
                    'chat_id': -11812986,
                }
        )

    def test_incorrect_text(self):
        request = webapp2.Request.blank("/")
        request.method = "POST"
        request.headers["Content-Type"] = "application/json"
        request.body = json.encode({
            'update': 1,
            'inline_query': {
                u'query': u'стртанный, ткест',
                u'from': {
                    u'username': u'm_messiah',
                    u'first_name': u'Maxim',
                    u'last_name': u'Muzafarov',
                    u'id': 3798371
                },
                u'id': "1",
                u'offset': 0,
            }
        })
        response = request.get_response(app)
        self.assertEqual(response.status_int, 200)
        self.assertIn("application/json", response.headers['Content-Type'])
        self.assertItemsEqual(
            json.decode(json.decode(response.body)['results']),
            [{
                u"message_text": u"\u0441\u0442\u0440\u0442\u0430\u043d\u043d\u044b\u0439, \u0442\u043a\u0435\u0441\u0442",
                u"type": u"article",
                u"id": u"0",
                u"title": u"YAspell",
                u"description": u"\u0441\u0442\u0440\u0442\u0430\u043d\u043d\u044b\u0439, \u0442\u043a\u0435\u0441\u0442"
            },
            {
                u'message_text': u'cnhnfyysq? nrtcn',
                u'title': u'qwerty',
                u'type': u'article',
                u'description': u'cnhnfyysq? nrtcn',
                u'id': u'1'
            },
            {
                u'message_text': u'cnhnfyysq^ nrtcn',
                u'title': u'mac',
                u'type': u'article',
                u'description': u'cnhnfyysq^ nrtcn',
                u'id': u'2'
            }]
        )
