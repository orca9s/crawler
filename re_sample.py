import re
# <a........>[내용]/a>
# 1. <a로 시작해서
# 2. >가 등장하기 전까지의 임의의 문자 "최소" 반복
# 3. >문자
# 4. <가 등장하기 전까지의 임의의 문자  "최소" 반복을 그룹화
# 5. </a>문자

with open('re.weekday_item_title.html', 'rt') as f:
    html = f.read()

# 정규 표현식 패턴(a태그이며, class="title"이 여는 태그에 포함되어 있을 경우, 해당 a태그의 내용부분을 구룹화)
p = re.compile(r'<a.*?>(.*?)</a>')
p = re.compile(r''' <a                     #<a로 시작하며
                    .*?class="title".*?>   #>가 등장하기 전까지의 임의의 문자 최소 반복, >까지
                    (.*?)                  # 임의의 문자반복
                    </a>                   # </a>가 나오기 전까지 ''', re.VERBOSE)
s = re.findall(p, html)

print(s)