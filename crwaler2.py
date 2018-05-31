import requests
from urllib.parse import urlparse
import os

r = urlparse('http://comic.naver.com/webtoon/detail.nhn/data/episode_list.html')

class Epiosode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_data):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_data = created_data

    @property
    def get_statements(self):
        if not os.path.exists(r'data/episode_list2.html'):
            payload = {'titleId': self.webtoon_id, 'no': self.no}
            r = requests.get('http://comic.naver.com/webtoon/list.nhn?', params=payload)
            print(r.url)
            with open('data/episode_list.html2', 'wt') as f:
                f.write(r.text)


class Webtoon:
    def __init__(self, webtoon_id, title, author, description, episode_list):
        self.webtoon_ide = webtoon_id
        self.title = title
        self.author = author
        self.description = description
        self.episode_list = list


