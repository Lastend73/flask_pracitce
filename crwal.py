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
    info_list = []
    more_button = driver.find_element(By.XPATH,f'//*[@id="screenMain"]/div/div[1]/div/ul/div/a[{num}]')
    href_value = more_button.get_attribute("href")
    driver.execute_script("window.open('" + href_value + "')")
    # print(f"num: {num}, href: {href_value}")
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
        option_name_filter = ["올리지오x", "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
        driver.implicitly_wait(5)

        info = []
        # 버튼 클릭하여 병원 정보 추출
        for a in range(len(price)) :
            option_delete_blank = option_name[a].text.replace(" ","")
            if "체험" in option_delete_blank or "첫방문" in option_delete_blank :
                print(option_delete_blank)
                continue
            for filter_word in option_name_filter:
                if filter_word in option_delete_blank and "+" not in option_delete_blank:
                    info.append([option_delete_blank,price[a].text[0:-1]])
                    break
                else :
                    print(option_delete_blank)

        more_button = driver.find_element(By.XPATH,'//*[@id="screenMain"]/div[1]/a/span/div')
        driver.execute_script("arguments[0].click();", more_button)

        hospital_name = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="hospital-page-text-title-hospitalname"]'))).text
        hospital_address_full = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'iMmBCJ '))).text
        hospital_address = hospital_address_full.split(" ")
        for b in info:
            b.insert(0,hospital_name)
            b.insert(1,hospital_address_full)
            if "서울" in hospital_address :
                b.insert(2,hospital_address[1])
            else :
                b.insert(2,hospital_address[0])
            
            info_list.append(b)

        #새 창 닫기
        driver.close()

        # 메인 창으로 전환
        driver.switch_to.window(main_window)
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
    product = "덴서티"
    driver = crwal.crwal_setting(f'https://www.gangnamunni.com/search?q={product}')

    move_event_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.kgpRaa')))
    driver.execute_script("arguments[0].click();", move_event_button)

    #스크롤 내리기 이동 전 위치
    scroll_location = driver.execute_script("return document.body.scrollHeight")
    event_count = int(driver.find_element(By.XPATH,'//*[@id="screenMain"]/div/h1/span').text.replace(",",""))
    # event_count = 20 
    print(event_count)
    if event_count > 20 :
        more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="screenMain"]/div/div[2]/button')))
        driver.execute_script("arguments[0].click();", more_button)
        print("A")

    driver = crwal.scroll(driver, scroll_location)

    main_window = driver.current_window_handle
    info_list = []
    count_num = 0
    refuse_num = 0
    
    for i in range(event_count):
        print(i)
        a = gangnamunni_crawl_data(driver,main_window,i+1)
        if a != None :
            info_list.extend(a)

        count_num = count_num + 1
        refuse_num = refuse_num + 1
        
        print(f"{count_num} / {event_count}")
        if refuse_num > 50 : 
            time.sleep(180)
            refuse_num = 0

    with open('강남언니.csv', 'w', encoding='cp949', newline='') as file:
        csv_writer = csv.writer(file) # 파일 객체를 csv.writer의 인자로 전달해 새로운 writer 객체를 생성
        csv_writer.writerow(['병원명', '병원주소', '지역','시술명','가격','옵션','샷수',"날짜"]) # 헤더 작성
        option_name_filter = ["올리지오x", "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
        
        for row in info_list :
            option_check = False
            for word in option_name_filter:
                if word in row[3]:
                    row.append(word)
                    option_check = True
                    break  # 일치하는 단어를 찾으면 반복문 종료
            if option_check == False:
                row.append("")    
            index = row[3].find("샷")
            if index != -1 :
                # 앞에 3글자 중 숫자만 추출
                shot_name = re.sub(r'[^0-9]', '', row[3][index-4:index])
            else :
                shot_name = ""
            row.append(shot_name)
            row.append(datetime.today().strftime("%Y-%m-%d"))
            csv_writer.writerow(row)

    driver.quit()
