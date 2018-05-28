# 우리가 웹 브라우저를 통해 보는 HTML문서는 GET 요청의 결과
# requests를 사용해 http://comic.naver.com/webtoon/weekdayList.nhn?week=주소에
# 요청 결과를 response변수에 할당해서 stastus_code속성을 출력
import requests

response = requests.get('http://comic.naver.com/webtoon/weekdayList.nhn?week=')
print(response.status_code)
print(response.text)

f = open('weekday.html', 'wt')
f.write(response.text)
f.close()

