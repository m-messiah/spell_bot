# coding=utf-8
import logging
from urllib import urlencode

import webapp2
from google.appengine.api import urlfetch
from webapp2_extras import json

__author__ = 'm_messiah'
__url__ = "https://spell-bot.appspot.com"
from re import compile
eng_letters = compile(r"[a-z]")

RUS = (1072, 1073, 1074, 1075, 1076, 1077, 1105, 1078, 1079, 1080, 1081, 1082,
       1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094,
       1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103)

ENG = (97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111,
       112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122)


def botan_track(chat_id, event, message):
    try:
        botan_url = "https://api.botan.io/track?"
        botan_url += "token=j_UZnN7wzukO2mVm0bhKntmBuuNsHEEZ&"
        botan_url += "uid=%s&" % chat_id
        botan_url += "name=%s" % event
        botan = urlfetch.fetch(botan_url,
                               payload=json.encode(message),
                               method=urlfetch.POST,
                               headers={"Content-Type": "application/json"})
        if botan.status_code == 200:
            response = json.decode(botan.content)
            if response['status'] == 'accepted':
                return True

        return False
    except:
        return False


def yaspell(text):
    try:
        yaspeller = urlfetch.fetch(
            'http://speller.yandex.net/services/spellservice.json/checkText',
            payload=urlencode({'text': text.encode("utf8")}),
            method=urlfetch.POST
        )
        correct_text = text
        if yaspeller.status_code == 200:
            for w in json.decode(yaspeller.content):
                try:
                    correct_text = correct_text.replace(w['word'], w['s'][0])
                except:
                    pass
        return correct_text
    except:
        return u""


def correct_spell(text):
    correct_text = yaspell(text)
    return {
        'type': 'article',
        'id': "0",
        'title': 'YAspell',
        'message_text': correct_text,
        'description': correct_text,
    }


def correct_qwerty_keymap(text):
    key = (113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 97, 115,
           100, 102, 103, 104, 106, 107, 108, 59, 39, 92, 60, 122, 120, 99,
           118, 98, 110, 109, 44, 46, 47, 96, 49, 50, 51, 52, 53, 54, 55, 56,
           57, 48, 45, 61, 126, 33, 64, 35, 36, 37, 94, 38, 42, 40, 41, 95,
           43, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 123, 125, 65, 83, 68,
           70, 71, 72, 74, 75, 76, 58, 34, 124, 62, 90, 88, 67, 86, 66, 78,
           77, 60, 62, 63)

    abc = (1081, 1094, 1091, 1082, 1077, 1085, 1075, 1096, 1097, 1079, 1093,
           1098, 1092, 1099, 1074, 1072, 1087, 1088, 1086, 1083, 1076, 1078,
           1101, 92, 47, 1103, 1095, 1089, 1084, 1080, 1090, 1100, 1073, 1102,
           46, 1105, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 1025, 33,
           34, 8470, 59, 37, 58, 63, 42, 40, 41, 95, 43, 1049, 1062, 1059,
           1050, 1045, 1053, 1043, 1064, 1065, 1047, 1061, 1066, 1060, 1067,
           1042, 1040, 1055, 1056, 1054, 1051, 1044, 1046, 1069, 47, 124,
           1071, 1063, 1057, 1052, 1048, 1058, 1068, 1041, 1070, 44)
    try:
        if eng_letters.search(text.lower()):
            abc, key = key, abc
        trans = dict(zip(abc, key))
        result = yaspell(text.translate(trans))
        return {
            'type': 'article',
            'id': "1",
            'title': 'qwerty',
            'message_text': result,
            'description': result,
        }
    except:
        return None


def correct_mac_keymap(text):
    key = (113, 119, 101, 114, 116, 121, 117, 105, 111, 112, 91, 93, 97,
           115, 100, 102, 103, 104, 106, 107, 108, 59, 39, 92, 96, 122,
           120, 99, 118, 98, 110, 109, 44, 46, 47, 167, 49, 50, 51, 52, 53,
           54, 55, 56, 57, 48, 45, 61, 177, 33, 64, 35, 36, 37, 94, 38, 42,
           40, 41, 95, 43, 81, 87, 69, 82, 84, 89, 85, 73, 79, 80, 123, 125,
           65, 83, 68, 70, 71, 72, 74, 75, 76, 58, 34, 124, 126, 90, 88, 67,
           86, 66, 78, 77, 60, 62, 63)

    abc = (1081, 1094, 1091, 1082, 1077, 1085, 1075, 1096, 1097, 1079, 1093,
           1098, 1092, 1099, 1074, 1072, 1087, 1088, 1086, 1083, 1076, 1078,
           1101, 1105, 93, 1103, 1095, 1089, 1084, 1080, 1090, 1100, 1073,
           1102, 47, 62, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 45, 61, 60,
           33, 34, 8470, 37, 58, 44, 46, 59, 40, 41, 95, 43, 1049, 1062,
           1059, 1050, 1045, 1053, 1043, 1064, 1065, 1047, 1061, 1066, 1060,
           1067, 1042, 1040, 1055, 1056, 1054, 1051, 1044, 1046, 1069, 1025,
           91, 1071, 1063, 1057, 1052, 1048, 1058, 1068, 1041, 1070, 63)
    try:
        if eng_letters.search(text.lower()):
            abc, key = key, abc
        trans = dict(zip(abc, key))
        result = yaspell(text.translate(trans))
        return {
            'type': 'article',
            'id': "2",
            'title': 'mac',
            'message_text': result,
            'description': result,
        }
    except:
        return None


class MainPage(webapp2.RequestHandler):
    def show_error(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode({
            'result': "Info",
            "name": "I am Spell bot (https://telegram.me/spell_bot)"
        }))

    def get(self):
        return self.show_error()

    def post(self):
        if 'Content-Type' not in self.request.headers:
            return self.show_error()
        if 'application/json' not in self.request.headers['Content-Type']:
            return self.show_error()
        try:
            update = json.decode(self.request.body)
        except Exception:
            return self.show_error()
        response = None
        logging.debug(update)
        if 'message' in update:
            message = update['message']
            if 'chat' in message and 'text' in message:
                if '/start' in message['text'] or '/help' in message['text']:
                    output = u"Привет! Я буду исправлять " \
                             u"твои ошибки в режиме inline"
                    botan_track(message['chat']['id'], '/start', message)
                    response = {'method': "sendMessage",
                                'chat_id': message['chat']['id'],
                                'text': output}
        elif 'inline_query' in update:
            message = update['inline_query']
            botan_track(message['from']['id'], 'inline', message)
            if len(message['query']) > 3:
                query_results = [correct_spell(message['query']),
                                 correct_qwerty_keymap(message['query']),
                                 correct_mac_keymap(message['query'])]
                response = {'method': 'answerInlineQuery',
                            'inline_query_id': message['id'],
                            'cache_time': 5,
                            'results': json.encode(query_results)}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.encode(response if response else {}))


app = webapp2.WSGIApplication([('/', MainPage)])

if __name__ == '__main__':
    app.run()