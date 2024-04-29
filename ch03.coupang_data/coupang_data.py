import platform
import subprocess
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import timedelta
from datetime import datetime as dt
from time import sleep
from bs4 import BeautifulSoup
import requests
import re

osName = platform.system()  # window 인지 mac 인지 알아내기 위한

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

# time 값 지정
LOADING_WAIT_TIME = 5
PAUSE_TIME = 0.5

# partner product info
product_name_lists = []  # 상품명
product_discount_rate_lists = []  # 할인률과 원래가격
product_price_lists = []  # 상품가격
product_arrival_time_lists = []  # 도착예정시간
product_rating_star_lists = []  # star 평가: ex.3.5
product_review_lists = []  # 상품리뷰 수
product_link_lists = []  # 상품 구매 링크
product_image_lists = []  # 상품 이미지

# 크롬 드라이버 디버거 모드
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
    # service = ChromeService('C:\\Users\\ree31\\.wdm\\drivers\\chromedriver\\win64\\124.0.6367.91\\chromedriver.exe')
    _driver = webdriver.Chrome(service=service, options=options)
    _driver.implicitly_wait(LOADING_WAIT_TIME)

    return _driver


def partner_coupang_selenium(driver):
    keyword = '자전거'
    
    driver.get(f'https://www.coupang.com/np/search?component=&q={keyword}&channel=user')
    sleep(LOADING_WAIT_TIME)
    
    html = driver.page_source
    # print(html, type(html))
    soup = BeautifulSoup(html, 'html.parser')
    
    # print(soup, type(soup))
    all_search_product_lists = soup.select('li.search-product')
    ad_search_product_lists = soup.select('li.search-product.search-product__ad-badge')
    
    # print(all_search_product_lists)
    
    rank_product_lists = []
    for product in all_search_product_lists:
        if product not in ad_search_product_lists:
            rank_product_lists.append(product)
            
    for inner in rank_product_lists:
        product_name = inner.select_one('div > div.name')
        if product_name is not None:
            product_name_lists.append(product_name.text.strip())
        else: 
            product_name_lists.append('No data')
    
    # print(product_name_lists)
    

def partner_coupang_requests():
    keyword = '자전거'
    url = f'https://www.coupang.com/np/search?component=&q={keyword}&channel=user'
    
    headers = {'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
               'Accept-Encoding': 'gzip'
               }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_search_product_lists = soup.select('li.search-product')  # 검색 상품 모두
    ad_search_product_lists = soup.select('li.search-product.search-product__ad-badge')  # 광고 상품만

    rank_product_lists = []
    for product in all_search_product_lists:
        if product not in ad_search_product_lists:
            rank_product_lists.append(product)
    
    for inner in rank_product_lists:
        product_name = inner.select_one('div > div.name')  # 상품명
        if product_name is not None:
            # print(product_name.text)
            product_name_lists.append(product_name.text.strip())
        else:
            product_name_lists.append('No data')
        product_discount_rate = inner.select_one('div.price-wrap > div.price > span.price-info')  # 할인률과 원래가격
        if product_discount_rate is not None:
            # print(product_discount_rate.text.lstrip())
            product_discount_rate_lists.append(f'{product_discount_rate.text.lstrip()}원')
        else:
            product_discount_rate_lists.append('No data')
        product_price = inner.select_one('div.price-wrap > div.price > em > strong')  # 상품가격
        if product_price is not None:
            # print(product_price.text.replace(",", ""))
            product_price_lists.append(f"{product_price.text}원")
        else:
            product_price_lists.append('No data')
        product_arrival_time = inner.select_one('div.price-wrap > div.delivery > span.arrival-info')  # 도착예정시간
        if product_arrival_time is not None:
            # print(product_arrival_time.text)
            product_arrival_time_lists.append(product_arrival_time.text)
        else:
            product_arrival_time_lists.append('No data')
        product_rating_star = inner.select_one(
            'div.other-info > div.rating-star > span.star > em.rating')  # star 평가: ex.3.5
        if product_rating_star is not None:
            # print(product_rating_star.text)
            product_rating_star_lists.append(product_rating_star.text)
        else:
            product_rating_star_lists.append('No data')
        product_review = inner.select_one('div.other-info > div > span.rating-total-count')  # 상품리뷰 수
        if product_review is not None:
            # print(re.sub("[()]", "", product_review.text))
            product_review_lists.append(re.sub("[()]", "", product_review.text))
        else:
            product_review_lists.append('0')

        product_link = inner.select_one('a.search-product-link')  # 상품 구매 링크
        try:
            p_link = "https://www.coupang.com" + product_link['data-product-link']
        except:
            p_link = "https://www.coupang.com" + product_link['href']
        product_link_lists.append(p_link)

        product_image = inner.select_one('img.search-product-wrap-img')
        p_image = product_image.get('data-img-src')
        if p_image is None:
            p_image = product_image.get('src')
            if 'https:' in p_image:
                print("https: 문구를 포함하고 있습니다.")  # 예외처리 가끔 https: 가 포함되어져 오는 경우
                p_image = f'{p_image}'
            else:
                p_image = f'https:{p_image}'
            # print(p_image)
            product_image_lists.append(p_image)
        else:
            if 'https:' in p_image:
                p_image = f'{p_image}'
                print("https: 문구를 포함하고 있습니다.")
            else:
                p_image = f'https:{p_image}'
            # print(p_image)
            product_image_lists.append(p_image)

    # 출력
    count = 1
    for product_name, product_discount_rate, product_price, product_arrival_time, product_rating_star, product_review, product_link, product_image in zip \
                (product_name_lists, product_discount_rate_lists, product_price_lists, product_arrival_time_lists,
                 product_rating_star_lists,
                 product_review_lists, product_link_lists, product_image_lists):
        print(
            f'{count}. {product_name} | {product_discount_rate} | {product_price} | {product_arrival_time} | {product_rating_star} | {product_review} | \n{product_link} | \n{product_image}\n')
        count = count + 1

# main start
if __name__ == '__main__':
    try:
        print("\nSTART...")
        start_time = time.time()  # 시작 시간 체크
        now = dt.now()
        print("START TIME : ", now.strftime('%Y-%m-%d %H:%M:%S'))
        
        # print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 시작]', C_END)
        # driver = init_driver()
        # sleep(PAUSE_TIME)
        # print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버 초기화 완료]', C_END)
        
        # print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버를 이용한 셀레니움 쿠팡파트너스 정보 가져오기 시작]', C_END)
        # partner_coupang_selenium(driver)
        # print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[크롬 드라이버를 이용한 셀레니움 쿠팡파트너스 정보 가져오기 완료]', C_END)
        
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[python requests 모듈(http 통신)을 이용한 쿠팡파트너스 정보 가져오기 시작]', C_END)
        partner_coupang_requests()
        print('\n' + C_BOLD + C_YELLOW + C_BGBLACK + '[python requests 모듈(http 통신)을 이용한 쿠팡파트너스 정보 가져오기 완료]', C_END)

    finally:
        # driver.close()  # 마지막 창을 닫기 위해서는 해당 주석 제거
        # driver.quit()
        end_time = time.time()  # 종료 시간 체크
        ctime = end_time - start_time
        time_list = str(timedelta(seconds=ctime)).split(".")
        print("\n실행시간(초)", ctime)
        print("실행시간 (시:분:초)", time_list)
        print("\nEND...")












