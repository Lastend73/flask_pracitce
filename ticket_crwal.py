from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from fake_useragent import UserAgent

import time
import csv
import re

from datetime import datetime
import pprint

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

async def get_data_from_yeosin():
    chrome_options = Options()
    # chrome_options.add_argument("headless")
    chrome_options.add_argument(f'user-agent={get_random_user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1024, 1080)
    driver.implicitly_wait(100)
    url = "https://www.yeoshin.co.kr/search/category?q=%EB%A6%AC%ED%94%84%ED%8C%85&tab=events"
    driver.get(url)

    #스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")


    driver.implicitly_wait(100)

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

    # 특정 클래스의 div 요소 찾기
    div_elements = driver.find_elements(By.CSS_SELECTOR, '#ct-view > div > main > article > section:nth-child(2) > section > div')
    print(f"Number of div elements with class 'your-class-name': {len(div_elements)}")

    # 창 이동
    for i in range(len(div_elements)-1):
        print(i)
        more_button = driver.find_element(By.XPATH,f'//*[@id="ct-view"]/div/main/article/section[2]/section/div[{i+1}]/article')
        driver.execute_script("arguments[0].click();", more_button)
        driver.implicitly_wait(100)
        # 모든 대상 div 요소 찾기
        div_price_CSS_SELECTOR = '.kOyfYG > div:nth-child(2) > div:nth-child(1)'
        div_option_CSS_SELECTOR = '.kOyfYG > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2)'
        div_title_CSS_SELECTOR = '#ct-view > div > div > div > div.sc-41b16511-1.bukNMr > div.sc-1543ab3d-0.sc-1543ab3d-1.sc-509fd85f-0.hQTMVb.bVOgYk.jlAXoU > article > div > div > p'
        div_address_CSS_SELECTOR = '#ct-view > div > div > div > div.sc-41b16511-1.bukNMr > div.sc-1543ab3d-0.sc-1543ab3d-1.sc-509fd85f-0.hQTMVb.bVOgYk.jlAXoU > article > section:nth-child(3) > div > div > span:nth-child(2)'
        
        div_elements_prices = driver.find_elements(By.CSS_SELECTOR, div_price_CSS_SELECTOR)
        div_elements_options = driver.find_elements(By.CSS_SELECTOR, div_option_CSS_SELECTOR)
        div_elements_title = driver.find_element(By.CSS_SELECTOR, div_title_CSS_SELECTOR).text
        div_elements_address = driver.find_element(By.CSS_SELECTOR, div_address_CSS_SELECTOR).text

        print(div_elements_title)
        print(div_elements_address)
        for i in range(len(div_elements_prices)):
            print(div_elements_prices[i].text)
            print(div_elements_options[i].text)
            

        # 각 div 요소의 텍스트 가져오기
        # for index, div_element in enumerate(div_elements):
        #     div_text = div_element.text
        #     print(f"Text in div {index + 1}: {div_text}")
        driver.implicitly_wait(100)
        # 뒤로 가기
        driver.back()

        # div 요소의 개수 출력
        # print(f"Number of div elements with class 'your-class-name': {len(div_elements)}")


    # Wait for the results to load
    time.sleep(3)

    # Close the browser
    driver.quit()