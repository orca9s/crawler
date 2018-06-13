import os

from urllib import parse

import requests
from bs4 import BeautifulSoup


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
        """
        self.webtoon_id, self.no 요소를 사용하여
        실제 에피소드 페이지 URL을 리턴해준
        :return:
        """
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }
        episode_url = url + parse.urlencode(params)
        return episode_url

    def get_image_url_list(self,):
        print('get_image_url_list strat')
        # 해당 에피소드의 이미지들의 URL문자열들을 리스트에 담아 리턴
        # 1. html 문자열 변수 할당
        # 파일명: episode_detail-{webtoon_id}-{episode_no}.html
        # 없으면 자신의 url property값으로 requests사용 결과를 저장
        # 2.soup객체 생성 후 파싱
        # div.wt_viewer의 자식 img 요소들의 src속성들을 가져옴
        # 적절히 list에 append하고 리턴하자

        # 웹툰 에피소드의 상세 페이지를 저장할 파일 경로
        # 웹툰의 고유ID와 에피소드의 고유ID를 사용해서 겹치지 않는 파일명을 만들어준다
        file_path = 'data/episode_detail-{webtoon_id}-{episode_no}.html'.format(
            webtoon_id=self.webtoon_id,
            episode_no=self.no,
        )
        print('file_path:', file_path)

        # 위 파일이 있는지 검사
        if os.path.exists(file_path):
            print('os.path.exists: True')
            # 있다면 읽어온 결과를 html변수에 할당
            html = open(file_path, 'rt').read()
        else:
            # 없다면 self.url에 requests를 사용해서 요청
            # 요청 결과를 html변수에 할당
            # 요청의 결과를 file_path에 해당하는 파일에 기록
            print('os.path.exists: False')
            print('http get request, url:', self.url)
            response = requests.get(self.url)
            html = response.text
            html = open(file_path, 'rt').write(html)

        # html문자열로 BeautifulSoup객체 생성
        soup = BeautifulSoup(html, 'lxml')

        # img목록을 찾는다. 위치는 "div.wt_viewer > img"
        img_list = soup.select('div.wt_viewer > img')

        # 이미지 URL(src의 값)을 저장할 리스트
        # url_list=[]
        # for img in img_lis:
        #   url_list.append(img.get('srt'))

        # img목록을 순회하며 각 itme(BeautifulSoup Tag object)에서
        # 'src'속성값을 사용해 리스트 생성
        return [img.get('src') for img in img_list]

    def download_all_images(self):
        for url in self.get_image_url_list():
            self.download(url)

    def download(self, url_img):
        """
        :param url_img: 실제 이미지의 URL
        :return:
        """
        # 서버에서 거부하지 않도록 HTTP헤더 중 'Rferer'항목을 채워서 요청
        url_referer = f'http://comic.naver.com/webtoon/list.nhn?titleId={self.webtoon_id}'
        headers = {
            'Referer': url_referer,
        }
        response = requests.get(url_img, headers=headers)

        # 이미지 URL에서 이미지명을 가져옴
        file_name = url_img.rsplit('/', 1)[-1]

        # 이미지가 저장될 폴더 경로, 폴더가 없으면 생성해준다
        dir_path = f'data/{self.webtoon_id}/{self.no}'
        os.makedirs(dir_path, exist_ok=True)
        # os.mkdir = 디렉터리를 생성한다.
        # os.rmdir = 디렉터리를 삭제한다. (단 디렉터리가 비어있어야 삭제 가능)
        # os.unlink = 파일을 지운다
        # os.rename(src, dfc) src라는 이름의 파일을 dfc이름으로 바꾼.
        # mkdir = 디렉터리를 생성하고 makedirs(exist_ok=True) 이미 디렉터리가 생성되어 있거나 권한이 없을경우 예외를 발생시킨다.

        # 이미지가 저장될 파일 경로, 'wb'모드로 열어 이진데이터를 기록한다.
        file_path = f'{dir_path}/{file_name}'
        open(file_path, 'wb').write(response.content)
        # 이진 데이터만 쓰


class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        self._title = None
        self._author = None
        self._description = None
        self._episode_list = list()
        self._html = ''

    def _get_info(self, attr_name):
        if not getattr(self, attr_name):
            self.set_info()
        return getattr(self, attr_name)

    @property
    def title(self):
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    @property
    def html(self):
        if not self._html:
            file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
            url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
            params = {
                'titleId': self.webtoon_id,
            }
            if os.path.exists(file_path):
                html = open(file_path, 'rt').read()
            else:
                response = requests.get(url_episode_list, params)
                print(response.url)
                html = response.text
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        """
        자신의 html 속성을 파싱한 결과를 사용해
        자신의 title, author, description속성값을 할당
        :return:
        """

        soup = BeautifulSoup(self.html, 'lxml')

        h2_title = soup.select_one('dib.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        soup = BeautifulSoup(self.html, 'lxml')
        table = soup.select_one('table.viewList')
        tr_list = table.select('tr')
        episode_list = list()
        for index, tr in enumerate(tr_list[1:]):
            if tr.get('class'):
                continue
            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            no = query_dict['no'][0]

            # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            # 현재 tr의 네 번째 td요소의 내용
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            new_episode = Episode(
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )
            episode_list.append(new_episode)
        self._episode_list = episode_list

    @property
    def episode_list(self):
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list


if __name__ == '__main__':
    webtoon1 = Webtoon(651673)
    print(webtoon1.title)
    print(webtoon1.author)
    print(webtoon1.description)
    e1 = webtoon1.episode_list[0]
    e1.download_all_images()
# if name main 쓰는 이유 모듈을 직접 실행시킬때 실행되게 하고싶으면 사용
#