# 오늘 할 것: 이미지도 가져오는 것 + 엑셀로 추출하는 것!

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# 라이브러리추가
# pip install xlsxwriter: 엑셀로 뽑게 해 주는 라이브러리
# pip install fake_useragent: 어떤 사이트에서 크롬유저를 막음 -> 나:크롬유저 -> 내가 크롬유저인 것을 속여주는 라이브러리

# 엑셀 처리 모듈 임포트
# pip install xlsxwriter
import xlsxwriter

# user_agent 정보를 변환해 주는 모듈 임포트
# 특정 브라우저로 크롤링을 진행할 때 차단되는 것을 방지
# pip install fake_useragent (필수 라이브러리까진 아님)
from fake_useragent import UserAgent

# 이미지를 바이트로 변환 처리 모듈
from io import BytesIO

# 요청 헤더 정보를 꺼내올 수 있는 모듈
import urllib.request as req # useragent와 연계해서 사용하려고!

d = datetime.today()

file_path = f'C:/test/알라딘 베스트셀러 1~400위_{d.year}_{d.month}_{d.day}.xlsx'

# User Agent 정보 변환 (필수는 아닙니다 근데 지금은 사용할 것임)
opener = req.build_opener() # 헤더 정보를 초기화
opener.addheaders = [('User-agent', UserAgent().edge)]
req.install_opener(opener) # 새로운 헤더 정보를 삽입
# 크롤링이 끝나지도 않았는데 꺼짐 -> 자동화 기능을 차단한 사이트 인 것을 인지
# 위의 설정을 통해 유저 정보를 속인다

# 엑셀 처리 선언
# Workbook 객체를 생성해서 엑셀 파일을 1개 생성해보자 (매개 값으로 저장 될 경로를 지정해준다)
workbook = xlsxwriter.Workbook(file_path) # file_path -> 미리 선언 해 놓은 경로

# 워크 시트 생성
worksheet = workbook.add_worksheet()

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

# 엑셀에 텍스트 저장
cell_format = workbook.add_format({'bold': True, 'font_color':'red', 'bg_color':'yellow'})
worksheet.write('A1', '썸네일', cell_format)
worksheet.write('B1', '제목', cell_format)
worksheet.write('C1', '작가', cell_format)
worksheet.write('D1', '출판사', cell_format)
worksheet.write('E1', '출판일', cell_format)
worksheet.write('F1', '가격', cell_format)
worksheet.write('G1', '링크', cell_format)
# 첫번째 행 설정(컬럼들)

# //*[@id="newbg_body"]/div[3]/ul/li[2]/a
# //*[@id="newbg_body"]/div[3]/ul/li[9]/a # for n in range(2, 10) 이렇게 해서 돌려주기 가능 or 무한루프가능

cur_page_num = 2 # 현재 페이지 번호
target_page_num = 9 # 목적 페이지 번호
rank = 1 #순위
cnt = 2 # 엑셀 행 수 카운트 해 줄 변수 (1은 컬럼명들임)

while True:
    #bs4 초기화
    soup = BeautifulSoup(brower.page_source, 'html.parser')

    div_ss_book_box_list = soup.find_all('div', class_='ss_book_box')

    # 이 for문은 50번 돈다 (: 50개 단위로 알라딘이 순위를 나눠놨음)
    for div_ss_book_box in div_ss_book_box_list:
        
        # 이미지 가져오기 -> 지목을 해야 가져올 수 있음
        # 이미지
        img_url = div_ss_book_box.select_one('table div > a img.front_cover') # select_one() : 1개만 선택해서 가져오는 것!
        # print(img_url)

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

        # 책 상세 정보 페이지 링크
        # title이라는 변수에 a태그를 지목해 놓은 상태
        # title -> a태그의 요소 전부를 가지고 있는 상태.
        # href로 작성된 키를 전달하고 해당 value를 받아 변수에 저장.
        page_link = title['href']

        # url에 달린 이미지 파일을 가지고 와서 바이트로 쪼갠 후 엑셀 파일로 쏠거임
        # 왜냐면 엑셀은 이미지 소스코드를 주거나 url을 준다고 띄워주는 프로그램이 아니기 때문에
        # 직접 바이트 단위로 쪼개서 엑셀에 쏴준다!
        try:
            # 이미지 바이트 처리
            # BytesIO 객체의 매개 값으로 아까 준비해 놓은 img 태그의 src값을 전달.
            BytesIO(req.urlopen(img_url['src'].read()))

            # 엑셀에 이미지 저장
            # worksheet.insert_image('배치할 셀 번호', 이미지 제목, {'image_data':바이트로 변환한 이미지, 추가하고 싶은 기타 속성들...})
            worksheet.insert_image(f'A{cnt}', img_url['src'], {'img_data':img_data, 'x_scale':0.5, 'y_scale':0.5})\
            
        except:
            '''
                파이썬에서는 블록 구조안에 아무것도 작성하지 않으면 !에러!가 발생
                블럭 구조 내부에 딱히 작성할 코드가 없어서 넘기고 싶을 땐,
                'pass' 라는 키워드를 사용한다.
            '''
            pass
        
        # 엑셀에 나머지 컬럼에 텍스트(책 제목, 가격, ...) 저장
        worksheet.write(f'B{cnt}', title.text)
        worksheet.write(f'C{cnt}', author_name)
        worksheet.write(f'D{cnt}', company)
        worksheet.write(f'E{cnt}', pub_day)
        worksheet.write(f'F{cnt}', price_data)
        worksheet.write(f'G{cnt}', page_link)

        # 다음 행으로~ (cnt가 한 행임)
        cnt += 1

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

brower.close()
workbook.close()