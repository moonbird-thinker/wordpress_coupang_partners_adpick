# -*- coding: utf-8 -*-

import subprocess
import datetime
import platform
import random
import time
from datetime import date
from datetime import timedelta
from datetime import datetime as dt
from time import gmtime
from time import sleep
from time import strftime
import chromedriver_autoinstaller
import pyshorteners
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os.path
from bs4 import BeautifulSoup
import time
import requests
import re
import os
import json
import hashlib
import hmac
from time import gmtime, strftime
from pprint import pprint as pp
from urllib.parse import urljoin
from urllib import parse
from urllib.parse import urlparse
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from dateutil.relativedelta import relativedelta
from urllib.request import urlopen
from tabulate import tabulate
import pandas as pd
from pathlib import Path
import urllib3
from itertools import product
import markdown
from requests_toolbelt.multipart.encoder import MultipartEncoder
import sys
import pickle

urllib3.disable_warnings()

osName = platform.system()

C_END = "\033[0m"
C_BOLD = "\033[1m"
C_INVERSE = "\033[7m"
C_BLACK = "\033[30m"
C_RED = "\033[31m"
C_GREEN = "\033[32m"
C_YELLOW = "\033[33m"
C_BLUE = "\033[34m"
C_PURPLE = "\033[35m"
C_CYAN = "\033[36m"
C_WHITE = "\033[37m"
C_BGBLACK = "\033[40m"
C_BGRED = "\033[41m"
C_BGGREEN = "\033[42m"
C_BGYELLOW = "\033[43m"
C_BGBLUE = "\033[44m"
C_BGPURPLE = "\033[45m"
C_BGCYAN = "\033[46m"
C_BGWHITE = "\033[47m"

sample_coupang_general_link = 'https://www.coupang.com/vp/products/1464545785?itemId=3757434107&vendorItemId=70808576328&q=%EC%9E%90%EC%A0%84%EA%B1%B0&itemsCount=36&searchId=752d9ba3463845e79a595eb2ef996eee&rank=1&isAddedCart='

# [사용자 입력 정보] ======================================================================================================== START

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15'
]
random_user_agent = random.choice(user_agents)
fixed_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'

# time 값 지정
LOADING_WAIT_TIME = 5
PAUSE_TIME = 0.5
LOGIN_WAIT_TIME = 180  # 로그인시 기다리는 시간

# 애드픽 쿠키를 저장하기 위한 패스 지정
COOKIES_SAVE_PATH = f'adpick_cookie_save'
# COOKIES_SAVE_PATH = f'/Users/xxx/Desktop/crawling/adpick_cookie_save'  # for mac

# [사용자 입력 정보] ======================================================================================================== END

# [시스템 공통 입력 정보] ======================================================================================================== START

# [시스템 공통 입력 정보] ======================================================================================================== END

def init_driver():
    if osName not in "Windows":
        try:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9231 --user-data-dir="~/Desktop/crawling/chromeTemp31"'],
                shell=True, stdout=subprocess.PIPE)  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen([
                '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9231 --user-data-dir="~/Desktop/crawling/chromeTemp31"'],
                shell=True, stdout=subprocess.PIPE)
    else:
        try:
            subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9231 '
                             r'--user-data-dir="C:\chrometemp31"')  # 디버거 크롬 구동
        except FileNotFoundError:
            subprocess.Popen(
                r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9231 '
                r'--user-data-dir="C:\chrometemp31"')

    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9231")

    service = ChromeService(executable_path=ChromeDriverManager().install())
    # service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\120.0.6099.71\\chromedriver.exe')
    _driver = webdriver.Chrome(service=service, options=options)
    _driver.implicitly_wait(LOADING_WAIT_TIME)
    return _driver


def get_cookies_session(driver, url):
    driver.get(url)
    sleep(LOADING_WAIT_TIME)

    _cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in _cookies:
        cookie_dict[cookie['name']] = cookie['value']
        print(f"{cookie['name']} = {cookie['value']}")

    _session = requests.Session()
    headers = {
        'User-Agent': fixed_user_agent,
    }

    _session.headers.update(headers)
    _session.cookies.update(cookie_dict)  # 응답받은 cookies로  변경
    # driver.close()
    # driver.quit()

    return _session


def adpick_login(driver):
    try:
        driver.get("https://www.adpick.co.kr/?ac=login")
        sleep(LOADING_WAIT_TIME)
        driver.find_element(By.ID, 'totalPointM')
        print(f'\n이미 로그인 되어 다음 과정으로 넘어가겠습니다.')
    except:
        driver.get("https://www.adpick.co.kr/?ac=login")
        sleep(LOADING_WAIT_TIME)

        print(f'\n{C_BOLD}{C_RED}{C_BGBLACK}[주의: 3분안에 로그인을 완료해주세요!!!]{C_END}')
        pbar = tqdm(total=LOGIN_WAIT_TIME)
        for x in range(LOGIN_WAIT_TIME):
            sleep(1)
            try:
                driver.find_element(By.ID, 'totalPointM')
                break
            except:
                pass
            pbar.update(1)
        pbar.close()


def check_domain_link(adpick_session, sample_coupang_general_link):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': random_user_agent,
    }
    
    params = {'md':'domain_check_mall', 'product_url':sample_coupang_general_link}

    with adpick_session as s:
        data = s.get('https://www.adpick.co.kr/apis/shopping.php', params=params, headers=headers).json()
        pp(data)
        
    return data['status']
    

def make_shopping_mate_adpick_link(adpick_session, sample_coupang_general_link):
    url = 'https://adpick.co.kr/apis/shopping.php'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': random_user_agent,
        'Referer': 'https://www.adpick.co.kr/?ac=link&tac=shopping&md=addlink'
    }

    # params 의 url 의 경우 , 콤마로 구분하여 여러개의 링크가 들어갈 수 있습니다.
    params = {'md': 'makeMultiProducturl',
              'urls': sample_coupang_general_link}
    with adpick_session as s:
        data = s.post(url, data=params, headers=headers).json()
        # pp(data)
        # print(data['time'])

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': random_user_agent,
        'Referer': 'https://www.adpick.co.kr/?ac=link&tac=shopping&md=addlink'
    }

    url = f"https://www.adpick.co.kr/apis/shopping.php?md=makeMultiProducturlList&time={data['time']}"
    with adpick_session as s:
        data = s.get(url, headers=headers).json()
        pp(data)

        apptitle = data['list'][0]['apptitle']  # 쿠팡, 11번가 등 파트너사 이름
        photo = data['list'][0]['photo'].replace('https://img.podgate.com/script/imageshop.php?f=', '')  # 상품에 대한 사진 링크
        product_name = data['list'][0]['product_name'].replace('+', '')  # 상품에 대한 이름
        product_price = '{0:,}'.format(int(data['list'][0]['product_price']))  # 상품에 대한 가격
        slink = data['list'][0]['slink']  # 상품에 대한 단축링크

        print(f'{apptitle} | {photo} | {product_name} | {product_price} | {slink}')


def get_adpick_session():
    try:
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
        driver = init_driver()
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
        
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[애드픽 로그인 시작(3분안에 로그인 해야 합니다.)]', C_END)
        adpick_login(driver)
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[애드픽 로그인 완료]', C_END)
        
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[로그인 후 쿠키값 저장 및 세션 리턴 시작]', C_END)
        adpick_session = get_cookies_session(driver, 'https://www.adpick.co.kr')
        sleep(PAUSE_TIME)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[로그인 후 쿠키값 저장 및 세션 리턴 완료]', C_END)
        
        return adpick_session, True
    except:
        return None, False

def init_session(retry):
    adpick_session = requests.session()
    if not os.path.exists(COOKIES_SAVE_PATH):
        Path(COOKIES_SAVE_PATH).touch(exist_ok=True)

    # 쿠키 불러오기
    if os.path.getsize(COOKIES_SAVE_PATH) > 0 and retry != 1:  # 파일안에 내용이 존재할때
        with open(COOKIES_SAVE_PATH, 'rb') as f:
            cookie_load = pickle.load(f)
        # 새로운 세션 생성
        saved_s = requests.session()

        # 기존에 있던 쿠키 불러오기
        saved_s.cookies.update(cookie_load)
        print(f'\nSaved Session : ', saved_s.cookies.get_dict())
        adpick_session = saved_s
    else:
        print(f'\nEmpty file or Expired Session')
        new_s, result = get_adpick_session()
        print(new_s)
        if result:
            print(f"\nSuccessful creation of new session")
            with open(COOKIES_SAVE_PATH, 'wb') as fc:
                pickle.dump(new_s.cookies, fc)
            print(f'\nNew Session : ', new_s.cookies.get_dict())
            adpick_session = new_s
        else:
            print(f"\nFailed to create a new session or other reason. please try again")
            sys.exit("exit...")

    return adpick_session
    

def get_adpick_mypoint_cache(adpick_session):
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
        'referer': 'https://www.adpick.co.kr/?ac=profile',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'ac': 'mypoint_cache',
    }

    with adpick_session as s:
        response = s.get(
            'https://www.adpick.co.kr/apis/income.php',
            params=params,
            headers=headers,
        )

        if response.ok:
            print(f'\nadpick nickname 얻기 완료 ok code:{response.status_code}')
            pp(response.json())
            return response.json()['data']
        else:
            print(f"\nadpick nickname 얻기 실패 fail code:{response.status_code} reason:{response.reason} msg:{response.text}")
            return None


# main start
if __name__ == '__main__':
    try:
        print("\nSTART...")
        start_time = time.time()  # 시작 시간 체크
        now = dt.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[애드픽 세션 정보 초기화 시작]{C_END}')
        adpick_session = init_session(0)
        sleep(PAUSE_TIME)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[애드픽 세션 정보 초기화 완료]{C_END}')
        
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[애드픽 세션 유지 확인 및 다시금 업데이트 시작]{C_END}')
        nickname = get_adpick_mypoint_cache(adpick_session)
        if nickname is not None:
            print(f'\n세션이 잘 유지되고 있습니다.')
        else:
            print('\n세션이 만료되었습니다. 업데이트를 하도록 하겠습니다.')
            adpick_session = init_session(1)
        print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[애드픽 세션 유지 확인 및 다시금 업데이트 완료]{C_END}') 
        
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[애드픽 파트너사 링크 첵크 시작]', C_END)
        ret = check_domain_link(adpick_session, sample_coupang_general_link)
        if ret != 1:
            print(f'\n정상적으로 변경할 수 없는 링크입니다.')
            sys.exit("exit...")
        else:
            make_shopping_mate_adpick_link(adpick_session, sample_coupang_general_link)
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[애드픽 파트너사 링크 첵크 완료]', C_END)
        
        

    finally:
        # driver.close()  # 마지막 창을 닫기 위해서는 해당 주석 제거
        # driver.quit()
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(timedelta(seconds=ctime)).split(".")
        print("\n실행시간(초)", ctime)
        print("실행시간 (시:분:초)", time_list)
        print("\nEND...")




