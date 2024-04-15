from datetime import datetime as dt
import requests
import json
from urllib.parse import urljoin
import base64
from requests.auth import HTTPBasicAuth

# https://blog.naver.com/moonbird_thinker/223142683391?trackingCode=blog_bloghome_searchlist
WP_URL = ''
WP_ID = ''
WP_BASIC_TOKEN = ''
WP_CATEGORY_ID = ''
WP_TAG_ID = ''

keys = {
    'wp_key': WP_BASIC_TOKEN,
    'user': WP_ID
}

# Define WP Keys
user = keys['user']
password = keys['wp_key']

# Create WP Connection
creds = user + ':' + password

# Encode the connection of your website
token = base64.b64encode(creds.encode())

# Prepare the header of our request
headers = {'Authorization': 'Basic ' + token.decode('utf-8')}

auth = HTTPBasicAuth(user, password)  # 위 과정이 이 한문장으로 변경이 가능 (auth=auth 로 사용해야함)

# # Define your WP URL
# media_url = f'{WP_URL}/wp-json/wp/v2/media'
#
# # 이미지 업로드
# files = {'file': open(image_file_name, 'rb')}
# # Prepare the header of our request
# response = requests.post(media_url, files=files, headers=headers)
#
# # 업로드된 이미지의 ID 가져오기
# if response.status_code == 201:
#     image_id = response.json()['id']
#     print('이미지가 성공적으로 업로드되었습니다.')
#     print('이미지 ID:', image_id)
# else:
#     print('이미지 업로드에 실패하였습니다.')
#     print('에러 메시지:', response.text)
#     exit()

status = 'publish'  # 즉시발행：publish, 임시저장：draft
slug = '슬러그 내용을 채워주세요'
title = '타이틀을 적어주세요'
content = '본문의 내용이 들어가면 됩니다'
description = '설명부분이 들어가게 됩니다.'

# 포스트 생성에 필요한 데이터(https://developer.wordpress.org/rest-api/reference/posts/)
data = {"status": status,
        "slug": slug,
        "title": title,
        "content": content,
        "date": dt.now().isoformat(),
        "categories": WP_CATEGORY_ID,
        "tags": WP_TAG_ID,
        # 'featured_media': image_id,  # 이미지 ID
        "excerpt": description
        #    "meta": {
        #         "description": "test description",
        #         "keywords": "test keywords",
        #         "filter": "raw"
        #         }
        }

# Define your WP URL
post_url = f'{WP_URL}/wp-json/wp/v2/posts'

# 포스트 생성 요청 보내기
response = requests.post(post_url, headers=headers, json=data)
# response = requests.post(post_url, json=data, auth=auth)

# 응답 결과 확인
if response.status_code == 201:
    post_id = response.json()['id']
    print(f'\n포스트가 성공적으로 생성되었습니다.')
    print('포스트 ID:', post_id)
else:
    print('포스트 생성에 실패하였습니다.')
    print(f'\n에러 메시지:', response.text.encode('utf-8').decode('unicode_escape'))