from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from fake_useragent import UserAgent

import crwal_setting as crwal

import time
import csv
import re

from datetime import datetime
import pprint

def gangnamunni_crawl_data(driver,main_window,num):
    option_name_filter = ["올리지오x", "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
    info_list = []
    more_button = driver.find_element(By.XPATH,f'//*[@id="event-card-component-ui-{num}"]')
    href_value = more_button.get_attribute("href")
    driver.execute_script("window.open('" + href_value + "')")
    print(f"num: {num}, href: {href_value}")
    driver.implicitly_wait(5)

    #창 현재창인지 확인
    for handle in driver.window_handles:
        if handle != main_window:
            driver.switch_to.window(handle)
            break

    #가격 및 옵션 추출
    try : 
        price = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cHFlCn')))
        option_name = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'hZkXMs')))
        
        driver.implicitly_wait(5)
        #병원명,병원주소,시술명,가격,url
        info = []
        url = driver.current_url
        print(url)
        # 버튼 클릭하여 병원 정보 추출
        for a in range(len(price)) :
            info.append([option_name[a].text, price[a].text[0:-1],url,"강남언니"])
            # option_delete_blank = option_name[a].text.replace(" ","")
            # if "체험" in option_delete_blank or "첫방문" in option_delete_blank :
            #     print(option_delete_blank)
            #     continue
            # for filter_word in option_name_filter:
            #     if filter_word in option_delete_blank and "+" not in option_delete_blank:
            #         break
            #     # else :
            #     #     print(option_delete_blank)

        more_button = driver.find_element(By.XPATH,'//*[@id="screenMain"]/div[1]/a/span/div')
        driver.execute_script("arguments[0].click();", more_button)

        hospital_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hospital-page-text-title-hospitalname"]'))).text
        hospital_address_full = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'iMmBCJ '))).text
        # hospital_address = hospital_address_full.split(" ")
        for b in info:
            b.insert(0,hospital_name)
            b.insert(1,hospital_address_full)


        #새 창 닫기
        driver.close()
        # 메인 창으로 전환
        driver.switch_to.window(main_window)
        return info
    except TimeoutException :
        print("스킵")
        #새 창 닫기
        driver.close()

        # 메인 창으로 전환
        driver.switch_to.window(main_window)
    except Exception :
        print("스킵")
        #새 창 닫기
        driver.close()

        # 메인 창으로 전환
        driver.switch_to.window(main_window)
    if info_list == [] :
        print("")
    else:    
        return info_list

def gangnamunni_crawl():
    #현재 창 저장
    info_list = []
    # for equipment_name in equipment_list:
    driver = crwal.crwal_setting(f'https://www.gangnamunni.com/events?q=%EB%A6%AC%ED%94%84%ED%8C%85')

    # move_event_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.kgpRaa')))
    # driver.execute_script("arguments[0].click();", move_event_button)

    #스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")
    # print(scroll_location)
    event_count = int(driver.find_element(By.CSS_SELECTOR,'.irAqsc').text.replace(",",""))
    # event_count = 20 
    print(event_count)
    if event_count > 20 :
        more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.kTmIRB ')))
        driver.execute_script("arguments[0].click();", more_button)
        print("A")

    driver = crwal.scroll(driver, scroll_location)

    main_window = driver.current_window_handle
    count_num = 0
    refuse_num = 0
    
    for i in range(event_count):
        print(i)
        a = gangnamunni_crawl_data(driver,main_window,i)
        if a != None :
            info_list.extend(a)

        count_num = count_num + 1
        refuse_num = refuse_num + 1
        
        print(f"{count_num} / {event_count}")
        if refuse_num > 50 : 
            time.sleep(180)
            refuse_num = 0
    driver.quit()
    return info_list
