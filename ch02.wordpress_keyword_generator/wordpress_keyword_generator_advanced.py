import subprocess
from time import sleep
import datetime
import time
import requests
import platform
import random
from tqdm import tqdm
from pprint import pprint as pp
from bs4 import BeautifulSoup
from datetime import timedelta
from urllib import parse
import pandas as pd
import os
from tabulate import tabulate
from itertools import product
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
import json
import ssl
import urllib3
import sys
import os.path
from pathlib import Path


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


ITEMSCOUT_CONVERSION_MAP_INFO_PATH = 'O:\workspace\wordpress_coupang_partners_adpick\ch02.wordpress_keyword_generator\itemscout_conversion_info.json'

fixed_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Whale/3.19.166.16 Safari/537.36'

def get_itemscout_cid_info():
    # File I/O Open function for read data from JSON File
    data = {}  # Define Empty Dictionary Object
    try:
        with open(ITEMSCOUT_CONVERSION_MAP_INFO_PATH) as file_object:
            data = json.load(file_object)  # _io.TextIOWrapper > dic
    except ValueError:
        print("Bad JSON file format,  Change JSON File")

    # pp(data)
    return [*data['data'].values()]  # list 로 반환
    

def get_items_for_itemscout(cid, duration, gender, ages):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://itemscout.io',
        'referer': 'https://itemscout.io/',
        'user-agent': fixed_user_agent,
    }

    data = {
        'duration': parse.quote(duration, encoding="utf-8"),  # url encoding 후 넣어줌
        'genders': parse.quote(gender, encoding="utf-8"),
        'ages': parse.quote(ages, encoding="utf-8")
    }

    response = requests.post(f'https://api.itemscout.io/api/category/{cid}/data', headers=headers, data=data, verify=False).json()
    # pp(response)

    for idx, item in enumerate(response['data']['data'].items()):
        # print(f'{item}')
        # print(f"keywordID(keyword ID): {item[0]}")  # keyword 아이디
        # print(f"rank(랭킹): {item[1]['rank']}")  # 랭킹
        # print(f"keyword(키워드): {item[1]['keyword']}")  # 키워드
        # print(f"total(검색수): {item[1]['monthly']['total']}")  # 검색수
        # print(f"prdCnt(상품수): {item[1]['prdCnt']}")  # 상품수

        try:
            print(
                f"{idx + 1}. ID {item[0]} | keyword {item[1]['keyword']} | 랭킹 {item[1]['rank']} | 검색수 {item[1]['monthly']['total']} | 상품수 {item[1]['prdCnt']}")
        except:
            print('ERROR : KeyError: "monthly"')
            continue
    


# main start
def main():
    try:
        start_time = time.time()  # 시작 시간 체크
        now = datetime.datetime.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nSTART...")
        
        random_itemscout_age_lists = ['10,10', '20,20', '30,30', '40,40', '50,50', '60,60', '10,20', '10,30', '10,40',
                                      '10,50', '10,60', '20,30', '20,40', '20,50', '20,60'
            , '30,40', '30,50', '30,60', '40,50', '40,60', '50,60']
        random_itemscout_gender_lists = ['f,m', 'f', 'm']  # 전체, 여성, 남성
        random_itemscout_cid_lists = get_itemscout_cid_info()
        
        random_itemscout_input_info_list = list(
            product(random_itemscout_cid_lists, random_itemscout_age_lists, random_itemscout_gender_lists))
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + f'[아이템스카우트 cid json 파일에서 읽어와 random input 값만들기 완료... 총 ({len(random_itemscout_input_info_list)})개의 조합]', C_END)
        
        for rnd_num in range(len(random_itemscout_input_info_list)):
            cid, age, gender = random.choice(random_itemscout_input_info_list)

            # 아이템스카우트 기간
            duration = '30d'  # (duration 30d 또는 날짜 설정, duration: 2023-03,2023-04 3월부터 4월)

            print(f'{C_BOLD}{C_YELLOW}{C_BGBLACK}RANDOM info >>> cid {cid} | duration {duration} | age {age} | gender {gender} {C_END}')
            
            print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 시작]{C_END}')
            get_items_for_itemscout(cid, duration, age, gender)
            print(f'\n{C_BOLD}{C_YELLOW}{C_BGBLACK}[itemscout 에서 아이템들 리스트를 전체 받기 완료]{C_END}')

    
    finally:
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(datetime.timedelta(seconds=ctime)).split(".")
        print("실행시간 (시:분:초)", time_list)
        now = datetime.datetime.now()
        print("END TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        print("\nEND...")
# main end


if __name__ == '__main__':
    main()