import os
import requests
from bs4 import BeautifulSoup

# HTML파일을 저장하거나 불러올 경로
file_path = 'data/episode_list.html'

# HTTP요청을 보낼 주소
url_episode_list = 'http://comic.naver.com/webtoon/list.nhn'
# HTTP요청시 전달할 GET parameters
paramas = {
    'titleId': 703845,
}

# -> 'http://com...nhn?titleId=703845

# HTML파일이 로컬에 저장되어 있는지 검사

if os.path.exists(file_path):
    # 저장되어 있다면, 해당 파일을 읽어서 html변수에 할당
    html = open(file_path, 'rt').read()
else:
    # 저장되어 있지 않다면, request를 사용해 HTTP get요청
    response = requests.get(url_episode_list, paramas)
    # 요청 응답객체의 text속성값을 html변수에 할당
    html = response.text
    # 받은 텍스트 데이터를 HTML파일로 저장
    open(file_path, 'wt').write(html)

# BeautifulSoup클래스형 객체 생성 및 soup변수에 할당
soup = BeautifulSoup(html, 'lxml')

# div.detail > h2 (제목, 작가)의
#  0번째 자식: 제목 텍스트
#  1번째 자식: 작가정보 span Tag
#   Tag로부터 문자열을 가져올때는 get_text()

h2_title = soup.select_one('div.detail > h2')
title = h2_title.contents[0].strip()
author = h2_title.contents[1].get_text(strip=True)
# div.detail > p (설명)
description = soup.select_one('div.detail > p').get_text(strip=True)

print(title)
print(author)
print(description)

# 3. 에피소드 정보 목록을 가져오기
#  url_thumbnail:   썸네일 URL
#  title:           제목
#  rating:          별점
#  created_date:    등록일
#  no:              에피소드 상세페이지의 고유 번호
#   각 에피소드들은 하나의 dict데이터
#   모든 에피소드들을 list에 넣는다

# 에피소드 목록을 담고 있는 table

table = soup.select_one('table.viewList')

# table 내의 모든 tr요소 목록
tr_list = table.select('tr')

# 첫 번째 tr은 thead의 tr이므로 제외, tr_list의 [1:]부터 순회
for index, tr in enumerate(tr_list[1:]):
    # 에피소드에 해당하는 tr은 클래스가 없으므로,
    # 현재 순회중인 tr요소가 클래스 속성값을 가진다면 continue
    if tr.get('class'):
        continue

    # 현재 tr의 첫 번째 td요소의 하위 img태그의 'src'속성값
    url_thumbnail = tr.select_one('td:nth-of-type(1) img').get('src')
    # 현재 tr의 첫 번째 td요소의 자식 a태그의 'href'속성
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

    print(title)
    print(no)
    print(rating)
    print(created_date)
    print(url_thumbnail)