'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# 라이브러리추가
# pip install xlsxwriter: 엑셀로 뽑게 해 주는 라이브러리
# pip install fake_useragent: 어떤 사이트에서 크롬유저를 막음 -> 나:크롬유저 -> 내가 크롬유저인 것을 속여주는 라이브러리


# user_agent 정보를 변환해 주는 모듈 임포트
# 특정 브라우저로 크롤링을 진행할 때 차단되는 것을 방지
# pip install fake_useragent (필수 라이브러리까진 아님)
from fake_useragent import UserAgent

# 요청 헤더 정보를 꺼내올 수 있는 모듈
import urllib.request as req # useragent와 연계해서 사용하려고!

# User Agent 정보 변환 (필수는 아닙니다 근데 지금은 사용할 것임)
opener = req.build_opener() # 헤더 정보를 초기화
opener.addheaders = [('User-agent', UserAgent().edge)]
req.install_opener(opener) # 새로운 헤더 정보를 삽입
# 크롤링이 끝나지도 않았는데 꺼짐 -> 자동화 기능을 차단한 사이트 인 것을 인지
# 위의 설정을 통해 유저 정보를 속인다

# 크롬 드라이버를 구동할 때 전달 할 옵션 설정.
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True) # 크롤링이 끝나고 나서도 브라우저가 계속 살아있게 만들어 줌

# 근데 난 브라우저가 뜨는 것 자체를 원하지 않음
# : 브라우저 안뜨게 하기
# options.add_argument('--headless')\

# 크롬 드라이버 버전을 관리 해 주는 객체를 선언 한 것임
# = 크롬 드라이버를 버전에 맞게 자동으로 지원해주는 객체
service = webdriver.ChromeService(ChromeDriverManager().install()) # 드라이버매니저 객체를 생성하고 install해주는 것임

# 크롬 드라이버 구동!
# 위에서 선언한 service와 options를 전달
brower = webdriver.Chrome(service=service, options=options)

# 브라우저 사이즈 조정
brower.set_window_size(800, 600)

# 페이지 이동을 시켜보자 (to 베스트셀러 페이지)
brower.get('https://www.melon.com/chart/index.htm')

# 브라우저 내부 대기 주기
# time.sleep(10) -> time은 브라우저 로딩에 상관 없이 무조건 10초 대기(왜냐면 CPU를 잠재우는 것이기 때문. 절대 시간)

# 웹 페이지 전체가 로딩될 때까지 대기 후 남은 시간 무시
brower.implicitly_wait(10)

# rank = 1

soup = BeautifulSoup(brower.page_source, 'html.parser')

while True:

    tbody_list = soup.find_all('tbody')
    rank = soup.find_all('tbody>tr td span.rank').text.strip()

    print(rank)

    for tbody in tbody_list:

        # 여기는 tr한개에 다 들어있음 1개의 tr지목
        tr = tbody.select_one('tbody > tr.lst50')

        # 노래 제목
        title = tr.select_one('td div.rank01>span>a').text
        
        # 가수 이름
        
        group = tr.select_one('td div.rank02>span>a').text

        # rank += 1

        if rank == 50:
            print('크롤링 종료!')
            break

print(tr, title, group)

brower.close()
'''

# 선생님 버전
# selenium import
from selenium import webdriver
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import urllib.request as req
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import codecs


d = datetime.today()

file_path = f'C:/test/멜론일간차트순위_{d.year}년{d.month}월{d.day}일{d.hour}시기준.txt'
# 헤더 정보 초기화
opener = req.build_opener()
# User Agent 정보
opener.addheaders = [('User-agent', UserAgent().edge)]
# 헤더 정보 삽입
req.install_opener(opener)


# 크롬 드라이버에게 전달할 옵션 설정.
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)


# 크롬 드라이버를 버전에 맞게 자동으로 지원해주는 객체
service = webdriver.ChromeService(ChromeDriverManager().install())

# 크롬 드라이버 구동
browser = webdriver.Chrome(service=service, options=options)

# 브라우저 사이즈 조정
browser.set_window_size(800, 600)

'''
- with문을 사용하면 with 블록을 벗어나는 순간
 객체가 자동으로 해제됩니다. (자바의 try with resource와 비슷)

- with 작성 시 사용할 객체의 이름을 as 뒤에 작성해 줍니다.
'''

with codecs.open(file_path, mode='w', encoding='utf-8') as f:

    # 페이지 이동
    target_page = 'https://www.melon.com/chart/day/index.htm'
    browser.get(target_page)

    soup = BeautifulSoup(browser.page_source, 'html.parser')

    for cnt in [50, 100]:

        song_tr_list = soup.select(f'#lst{cnt}')

        for song_tr in song_tr_list:

            # 순위 찾기
            rank = song_tr.select_one('div.wrap.t_center').text.strip()
            print(rank)

            # 가수 이름 찾기
            artist_name = song_tr.select_one('div.wrap div.ellipsis.rank02 > a').text.strip()
            print(artist_name)

            # 앨범명 찾기
            album_name = song_tr.select_one('div.wrap div.ellipsis.rank03 > a').text.strip()
            print(album_name)

            # 노래명 찾기
            song_name = song_tr.select_one('div.wrap div.ellipsis.rank01 > span > a').text.strip()
            print(song_name)


            print("=" * 40)

            f.write(f'# 순위: {rank}\n')
            f.write(f'# 가수명: {artist_name}\n')
            f.write(f'# 앨범명: {album_name}\n')
            f.write(f'# 노래 제목: {song_name}\n')
            f.write('-' * 40 + '\n')


browser.close()