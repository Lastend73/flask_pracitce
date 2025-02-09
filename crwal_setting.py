from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from fake_useragent import UserAgent

import time
import csv
import re

from datetime import datetime

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def crwal_setting(url): 
    chrome_options = Options()
    # chrome_options.add_argument("headless")
    # chrome_options.add_argument(f'user-agent={get_random_user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1024, 1080)
    driver.implicitly_wait(100)
    driver.get(url)

    return driver

def scroll(driver, scroll_location):
    while True:
        #현재 스크롤의 가장 아래로 내림
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

        #전체 스크롤이 늘어날 때까지 대기
        time.sleep(1)

        #늘어난 스크롤 높이
        scroll_height = driver.execute_script("return document.body.scrollHeight")

        #늘어난 스크롤 위치와 이동 전 위치 같으면(더 이상 스크롤이 늘어나지 않으면) 종료
        if scroll_location == scroll_height:
            print(scroll_location)
            print(scroll_height)
            break

        #같지 않으면 스크롤 위치 값을 수정하여 같아질 때까지 반복
        else:
            #스크롤 위치값을 수정
            scroll_location = driver.execute_script("return document.body.scrollHeight")
    return driver

def make_to_csv(info_list):
    # [병원명, 병원주소, 지역, 시술명, 가격, 옵션, 샷수, 날짜]
    with open('강남언니2.csv', 'w', encoding='cp949', newline='') as file:
        csv_writer = csv.writer(file) # 파일 객체를 csv.writer의 인자로 전달해 새로운 writer 객체를 생성
        csv_writer.writerow(['병원명', '병원주소', '시술명', '샷수', '가격', 'url', '사이트' ,'날짜', '옵션']) # 헤더 작성
        option_name_filter = ["올리지오x", "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
        
        # ['병원명', '병원주소', '시술명', '샷수', '가격', 'url', '사이트' ,'날짜', '옵션']
        for row in info_list :
            # 옵션명 공백 제거
            row[2]=row[2].replace(" ","")
            
            # 샷수 추출
            index = row[2].find("샷")
            if index != -1 :
                # 앞에 3글자 중 숫자만 추출
                shot_name = int(re.sub(r'[^0-9]', '', row[2][index-4:index]))
            else :
                shot_name = ""
            row.insert(3,shot_name)

            # 날짜 추가
            row.append(datetime.today().strftime("%Y-%m-%d"))

        for row in info_list :
            if "+"in row[2]:
                continue
            if row[3] == "":
                continue


            # option_check = False
            # for word in option_name_filter:
            #     if word in row[3]:
            #         row.append(word)
            #         option_check = True
            #         break  # 일치하는 단어를 찾으면 반복문 종료
            # if option_check == False:
            #     row.append("")    
            # index = row[3].find("샷")
            # if index != -1 :
            #     # 앞에 3글자 중 숫자만 추출
            #     shot_name = int(re.sub(r'[^0-9]', '', row[3][index-4:index]))
            # else :
            #     shot_name = ""
            # row.append(shot_name)
            # row.append(datetime.today().strftime("%Y-%m-%d"))
            # print(row)
            csv_writer.writerow(row)
