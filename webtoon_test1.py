from urllib import parse


def webtoon_crawler(webtoon_id):
    '''
    webtoon_id 매개변수를 이용하여
    웹툰, title, author, description을 딕셔너리 형태로 return
    :param webtoon_id:
    :return:title, author, description 딕셔너리로
    '''
    # HTML 파일을 저장하거나 불러올 경로
    file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=webtoon_id)
    # HTTP 요청을 보낼 주소

class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail, title, rating, created_date):
        self.webtoon_id = webtoon_id
        self.no = no
        self.url_thumbnail = url_thumbnail
        self.title = title
        self.rating = rating
        self.created_date = created_date

    @property
    def url(self):
        '''
        self.webtoon_id, self.no 요소를 사용하여
        실제 에피소드 페이지 URL을 리턴한다.
        :return:
        '''
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        # webtoon 속성 채우기 위해 webtoon_crawler() 실행
        # webtoon_crawler 함수 결과 dict()
        info = webtoon_crawler(webtoon_id)
        self.title = info['title']
        self.author = info['author']
        self.description = info['description']
        self.episode_list = list()

    def update(self):
        '''

        :return:
        '''