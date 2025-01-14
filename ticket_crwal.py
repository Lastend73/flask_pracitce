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
import crwal_setting as crwal

from datetime import datetime

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_data_from_yeosin(product):
    url = f"https://www.yeoshin.co.kr/search/category?q={product}&tab=events"
    driver = crwal.crwal_setting(url)

    scroll_location = driver.execute_script("return document.body.scrollHeight")
    driver =  crwal.scroll(driver, scroll_location)

    # 특정 클래스의 div 요소 찾기
    div_elements = driver.find_elements(By.CSS_SELECTOR, '.krWpkt')
    print(f"Number of div elements with class 'your-class-name': {len(div_elements)}")

    # 창 이동
    for i in div_elements:
        info_list = []
        more_button = driver.find_element(By.CSS_SELECTOR,f'.krWpkt')
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
        # [병원명, 병원주소, 지역, 시술명, 가격, 옵션, 샷수, 날짜]
        for i in range(len(div_elements_prices)):
            print(div_elements_prices[i].text)
            print(div_elements_options[i].text)
            info_list.append([div_elements_title, div_elements_address, product, div_elements_prices[i].text, div_elements_options[i].text, "1", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

        driver.implicitly_wait(100)
        # 뒤로 가기
        driver.back()

        # div 요소의 개수 출력
        # print(f"Number of div elements with class 'your-class-name': {len(div_elements)}")


    # Wait for the results to load
    time.sleep(3)

    # Close the browser
    driver.quit()