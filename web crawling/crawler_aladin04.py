
# DB에 크롤링 데이터 넣기
'''
    라이브러리 필요
    mysql과 python을 연결 해 주는 라이브러리
    1. mysql-connector-python
    2. pymysql
    1번을 cmd에서 pip install mysql-connector-python 해줬다!
'''

# 오늘 할 것: 이미지도 가져오는 것 + 엑셀로 추출하는 것!

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

import mysql.connector

# DB접속을 위한 정보 세팅
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='mysql',
    database='jpa'
)

# sql 실행을 위한 커서 생성
mycursor = mydb.cursor()

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
brower.get('https://www.aladin.co.kr/shop/common/wbest.aspx?BranchType=1&start=we')

# 브라우저 내부 대기 주기
# time.sleep(10) -> time은 브라우저 로딩에 상관 없이 무조건 10초 대기(왜냐면 CPU를 잠재우는 것이기 때문. 절대 시간)

# 웹 페이지 전체가 로딩될 때까지 대기 후 남은 시간 무시
brower.implicitly_wait(10)

cur_page_num = 2 # 현재 페이지 번호
target_page_num = 9 # 목적 페이지 번호
rank = 1 #순위

while True:
    #bs4 초기화
    soup = BeautifulSoup(brower.page_source, 'html.parser')

    div_ss_book_box_list = soup.find_all('div', class_='ss_book_box')

    # 이 for문은 50번 돈다 (: 50개 단위로 알라딘이 순위를 나눠놨음)
    for div_ss_book_box in div_ss_book_box_list:
        
        # 타이틀, 작가, 가격정보를 모두 포함하는 ul부터 지목
        ul = div_ss_book_box.select_one('div.ss_book_list > ul')

        # 타이틀
        title = ul.select_one('li > a.bo3')

        # 작가 이름
        # 위에서 얻은 title의 부모요소 li의 다음 형제 li를 지목 -> 작가, 출판사, 출판일 존재
        author = title.find_parent().find_next_sibling()

        # 작가 쪽 영역 데이터 상세 분해
        author_data = author.text.split('|')
        author_name = author_data[0].strip()
        company = author_data[1].strip()
        pub_day = author_data[2].strip()

        # 가격
        price = author.find_next_sibling()
        price_data = price.text.split(', ')[0]

        # 여기서부턴 크롤링 데이터들이 세팅이 완료 되었음
        # sql을 문자열로 작성하고 우리가 삽입하고자 하는 변수가 들어 갈 위치를 %s로 표현합니다.
        # 값은 tuple로 순서대로 세팅해서 전달합니다.
        # %s 작성 이유 -> 어차피 변수의 값을 넣을 것이기 때문에 문자의 타입을 따져서 작성하지 않았다
        query = 'INSERT INTO tbl_crawling (data_rank, title, author, company, publish_date, price) VALUES (%s, %s, %s, %s, %s, %s)'
        values = (rank, title.text, author_name, company, pub_day, price_data)

        mycursor.execute(query, values)

        rank += 1

    # 다음 페이지(탭 / 다음 순위)로 전환
    cur_page_num += 1
    # 옆의 탭의 XPATH를 가져온다.
    # //*[@id="newbg_body"]/div[3]/ul/li[3]/a
    brower.find_element(By.XPATH, f'//*[@id="newbg_body"]/div[3]/ul/li[{cur_page_num}]/a').click()
    
    # del: delete기능을 해주는 내장 함수
    # soup: 첫 페이지의 html소스코드를 담고 있는 객체
    del soup # 다음 페이지로 넘어가기 전에 그냥 soup를 정리 해 주는 것임
    brower.implicitly_wait(3)

    if cur_page_num == target_page_num:
        print('크롤링 종료!')
        break # while True의 break
    
    mydb.commit()
    mydb.rollback #문제 발생 시 예외처리와 함께 사용해서, 중간에 에러 발생 시 롤백 가능

brower.close()
mycursor.close()
mydb.close()