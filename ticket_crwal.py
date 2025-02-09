from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from fake_useragent import UserAgent

import time
import math
import crwal_setting as crwal


def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_data_from_yeosin(equipment_list):
    for equipment in equipment_list:
        url = f"https://www.yeoshin.co.kr/search/category?q={equipment}&tab=events"
        driver = crwal.crwal_setting(url)

        scroll_location = driver.execute_script("return document.body.scrollHeight")
        driver =  crwal.scroll(driver, scroll_location)

        # 특정 클래스의 div 요소 찾기
        div_elements =  driver.find_elements(By.CSS_SELECTOR, "[data-testid='virtuoso-item-list']>div")
        max_index = -1
        for div in div_elements:
            index_value = int(div.get_attribute('data-index'))
            if index_value > max_index:
                max_index = index_value
        print(f"Number of div elements with class 'your-class-name': {max_index}")
        scroll_location = driver.execute_script("return document.body.scrollHeight") #현재 스크롤 위치 저장
        driver.execute_script("window.scrollTo(0, 0);") #스크롤 위치 초기화
        print(scroll_location)

        total_height=0
        info_list = []
        # 창 이동
        for i in range(max_index+1):
            # more_button = driver.find_element(By.CSS_SELECTOR,f'.krWpkt')
            print(i)
            button = driver.find_element(By.CSS_SELECTOR, f"[data-index='{i}']>article")
            height = int(driver.find_element(By.CSS_SELECTOR, f"[data-index='{i}']").get_attribute('data-known-size'))
            total_height += height
            driver.execute_script("arguments[0].click();", button)
            driver.implicitly_wait(100)
            # 모든 대상 div 요소 찾기
            div_price_CSS_SELECTOR = '.kOyfYG > div:nth-child(2) > div:nth-child(1)'
            div_option_CSS_SELECTOR = '.kOyfYG > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2)'
            div_title_Xpath = '//*[@id="ct-view"]/div/div/div/div[2]/div[1]/article/div/div/p'
            div_address_Xpath = '//*[@id="ct-view"]/div/div/div/div[2]/div[1]/article/section[2]/div/div/span[1]'
            
            div_elements_prices = driver.find_elements(By.CSS_SELECTOR, div_price_CSS_SELECTOR)
            div_elements_options = driver.find_elements(By.CSS_SELECTOR, div_option_CSS_SELECTOR)

            div_elements_title = driver.find_element(By.XPATH, div_title_Xpath).text
            div_elements_address = driver.find_element(By.XPATH, div_address_Xpath).text

            print(div_elements_title)
            print(div_elements_address)
            # [병원명, 병원주소, 시술명, 가격,위치치]
            for i in range(len(div_elements_prices)):
                print(div_elements_prices[i].text)
                print(div_elements_options[i].text)
                url = driver.current_url
                info_list.append([div_elements_title, div_elements_address, div_elements_options[i].text, div_elements_prices[i].text[0:-1], url,"여신티켓"])
            driver.implicitly_wait(100)
            # 뒤로 가기
            driver.back()
            time.sleep(1)
            height_count = math.ceil(total_height/500)
            for i in range(height_count): #
                driver.execute_script(f"window.scrollTo(0, {i*500});") #스크롤 170만큼 내림
            time.sleep(1)
            
        


        # Wait for the results to load
        time.sleep(3)

        # Close the browser
        driver.quit()

        return info_list