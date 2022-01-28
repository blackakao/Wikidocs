from operator import truediv
from selenium import webdriver
import time


# 웹페이지 멈추기
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])


# 브라우저 오픈
driver = webdriver.Chrome('E:\WindowApps\chromedriver_win32\chromedriver.exe')
driver.implicitly_wait(20)

# 케어포 이동
driver.get('https://www.longtermcare.or.kr')
driver.implicitly_wait(10)



# 지점별 로그인 아이디 다른 경우
branch_code = '14128001166'
id = '이찬재'
id2 = '이샛별'
id3 = '박은경'
pwd = '*wkdtnakst1'

# 일단 일산본점 로그인 정보 입력
driver.find_element_by_name('ctmnumb').send_keys(branch_code)
driver.find_element_by_name('stmiden').send_keys(id)
driver.find_element_by_name('stmpass').send_keys(pwd)

# 로그인 버튼 클릭
driver.find_element_by_class_name('btn').click()

    





