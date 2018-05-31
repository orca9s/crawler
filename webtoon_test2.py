import os
from urllib import parse

import requests
from bs4 import BeautifulSoup


class Episode:
    def __init__(self, webtoon_id, no, url_thumbnail,
                 title, rating, created_date):
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
        실제 에피소드 페이지 URL을 리턴
        :return:
        """
        url = 'http://comic.naver.com/webtoon/detail.nhn?'
        params = {
            'titleId': self.webtoon_id,
            'no': self.no,
        }

        episode_url = url + parse.urlencode(params)
        return episode_url

    def get_image_url_list(self):
        print('get_image')
        # 해당 에피소드의 이미지들의 URL문자열들을 리스트에 담아 리턴
        # 1. html 문자열 변수 할당
        #  파일명 : episode_detail-{
        # 2. soup객체 생성 후 파싱
        # div.wt_viewer의 자식 img요소들의 src속성들을 가져옴
        # 적절히 list에 append하고 리턴하자
        file_path = 'data/episode_detail-{webtoon_id}-{episode_no}.html'.format(
            webtoon_id=self.webtoon_id,
            episode_no=self.episode_no,
        )
        print('file_path:', file_path)
        if os.path.exists(file_path):
            print('os.path.exits: True')
            html = open(file_path, 'rt').read()
        else:
            print('os.path.exists: False')
            print('http get request, url:', self.url)
            response = requests.get(self.url)
            html = response.text
            open(file_path, 'wt').write(html)
        # html 문자열로 BeautifulSoup객체 생성
        soup = BeautifulSoup(html, 'lxml')

        # img목록을 찾는다. 위치는 "div.wt_viewer > img "
        img_list = soup.select('div.wt_viewer > img')

        # 이미지 URL(src의 값)을 저장할 리스트
        # url_list = []
        # for img in inm_list:
        #      url_list.append(img.get('src'))

        # img 목록을 순회하며 각 item(BeautifulSoup Tag object)에서
        # 'src'속성값을 사용해 리스트 생성
        return [img.get('src') for img in img_list]



class Webtoon:
    def __init__(self, webtoon_id):
        self.webtoon_id = webtoon_id
        # webtoon 속성 채우기 위해 set_info() 실행
        # set_info 함수 결과 dict()
        # info = self.set_info()
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
        # 인스턴스에게 title속성값이 존재하면 그걸 리턴
        # 없으면 set_info()를 호출 후에 인스턴스의 title값을 리턴
        return self._get_info('_title')

    @property
    def author(self):
        return self._get_info('_author')

    @property
    def description(self):
        return self._get_info('_description')

    @property
    def html(self):
        # get_html의 결과 문자열을
        # 인스턴스가 갖고 있을 수 있도록 설정
        # 1. 인스턴스가 html데이터를 갖고 있지 않을 경우
        #    인스턴스의 html속성에 데이터 할당
        # 2. 갖고있으면
        #    인스턴스의 html속성을 리턴
        # HTML파일을 저장하거나 불러올 경로
        file_path = 'data/episode_list-{webtoon_id}.html'.format(webtoon_id=self.webtoon_id)
        # HTTP요청을 보낼 주소
        url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
        # HTTP요청시 전달할 GET Parameters
        params = {
            'titleId': self.webtoon_id,
        }
        # -> 'http://com....nhn?titleId=703845

        if not self._html:
            # 인스턴스의 html속성값이 False(빈 문자열)일 경우
            # HTML파일이 로컬에 저장되어 있는지 검사
            if os.path.exists(file_path):
                # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
                html = open(file_path, 'rt').read()
            else:
                # 저장되어 있지 않다면, requests를 사용해 HTTP GET요청
                response = requests.get(url_episode_list, params)
                print(response.url)
                # 요청 응답객체의 text속성값을 html변수에 할당
                html = response.text
                # 받은 텍스트 데이터를 HTML파일로 저장
                open(file_path, 'wt').write(html)
            self._html = html
        return self._html

    def set_info(self):
        """
        자신의 html속성을 파싱한 결과를 사용해
        자신의 title, author, descriptiont 속성값을 할당
        """

        # 공통함수는 html을 리턴하도록 한다
        # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
        soup = BeautifulSoup(self.html, 'lxml')

        # 파일 저장하지 않고 진행하고 싶은 경우
        # 위에 코드를 다 주석으로 변경
        # 파일 저장안해도 되는 경우
        # url = 'http://comic.naver.com/webtoon/list.nhn'
        # params = {
        #     "titleId": webtoon_id
        # }
        # response = requests.get(url, params)
        # print(response.url)
        # soup = BeautifulSoup(response.text, 'lxml')

        # div.detail > h2 (제목, 작가)의
        #  0번째 자식: 제목 텍스트
        #  1번째 자식: 작가정보 span Tag
        #   Tag로부터 문자열을 가져올때는 get_text()
        h2_title = soup.select_one('div.detail > h2')
        title = h2_title.contents[0].strip()
        author = h2_title.contents[1].get_text(strip=True)
        # div.detail > p (설명)
        description = soup.select_one('div.detail > p').get_text(strip=True)

        # webtoon title, author, description
        # # 딕셔너리 형태로 return
        # info = dict()
        # info['title'] = title
        # info['author'] = author
        # info['description'] = description
        # return info
        # 자신의 html데이터를 사용해서 (웹에서 받아오거나, 파일에서 읽어온 결과)
        # 자신의 속성들을 지정
        self._title = title
        self._author = author
        self._description = description

    def crawl_episode_list(self):
        """
        자기자신의 webtoon_id에 해당하는 HTML
        :return: Episode 인스턴스가 저장되어있는 List
        """
        # BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
        soup = BeautifulSoup(self.html, 'lxml')

        # 파일 저장안해도 되는 경우
        # 파일 저장하지 않고 실행하고 싶다면 위의 코드를 주석처리후 사용할것!
        # url = 'http://comic.naver.com/webtoon/list.nhn'
        # params = {
        #     "titleId": webtoon_id
        # }
        # response = requests.get(url, params)
        # print(response.url)
        # soup = BeautifulSoup(response.text, 'lxml')

        # 에피소드 목록을 담고 있는 table
        table = soup.select_one('table.viewList')
        # table내의 모든 tr요소 목록
        tr_list = table.select('tr')
        # list를 리턴하기 위해 선언
        # for문을 다 실행하면 episode_lists 에는 Episode 인스턴스가 들어가있음
        episode_list = list()
        # 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
        for index, tr in enumerate(tr_list[1:]):
            # 에피소드에 해당하는 tr은 클래스가 없으므로,
            # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
            if tr.get('class'):
                continue

            # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
            url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
            # 현재 tr의 첫 번째 td요소의 자식   a태그의 'href'속성값
            from urllib import parse
            url_detail = tr.select_one('td:nth-of-type(1) > a').get('href')
            query_string = parse.urlsplit(url_detail).query
            query_dict = parse.parse_qs(query_string)
            # print(query_dict)
            no = query_dict['no'][0]

            # 현재 tr의 두 번째 td요소의 자식 a요소의 내용
            title = tr.select_one('td:nth-of-type(2) > a').get_text(strip=True)
            # 현재 tr의 세 번째 td요소의 하위 strong태그의 내용
            rating = tr.select_one('td:nth-of-type(3) strong').get_text(strip=True)
            # 현재 tr의 네 번째 td요소의 내용
            created_date = tr.select_one('td:nth-of-type(4)').get_text(strip=True)

            # 매 에피소드 정보를 Episode 인보스턴스로 생성
            # new_episode = Episode 인스턴스
            new_episode = Episode(
                webtoon_id=self.webtoon_id,
                no=no,
                url_thumbnail=url_thumbnail,
                title=title,
                rating=rating,
                created_date=created_date,
            )

            # episode_lists Episode 인스턴스들 추가
            episode_list.append(new_episode)
        self._episode_list = episode_list

    @property
    def episode_list(self):
        # self.episode_list가 빈 리스트가 아니라면
        #  ->self.episode_list를 반환
        # self.episode_list가 비어있다면
        # 채우는 함수를 실행해서 self.episode_list리스트에 값을 채운 뒤
        # self._episode_list를 반환
        # if len(self.episode_list) == 0:
        #     self.crawl_episode_list()
        # else:
        #     return self.episode_list
        if not self._episode_list:
            self.crawl_episode_list()
        return self._episode_list


if __name__ == '__main__':
    webtoon1 = Webtoon(703845)
    print(webtoon1.title)
    print(webtoon1.author)
    print(webtoon1.description)
    for episode in webtoon1.episode_list:
        print(episode.title)
