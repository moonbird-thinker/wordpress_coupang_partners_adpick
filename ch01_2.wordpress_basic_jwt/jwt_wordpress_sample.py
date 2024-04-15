from datetime import datetime as dt
import requests
import json
from urllib.parse import urljoin

# https://blog.naver.com/moonbird_thinker/223142683391?trackingCode=blog_bloghome_searchlist
WP_URL = ''
WP_JWT_TOKEN = ''
WP_CATEGORY_ID = ''
WP_TAG_ID = ''

# headers = {
#     "Authorization": "Bearer %s" % WP_JWT_TOKEN,
# }

# # Define your WP URL
# media_url = f'{WP_URL}/wp-json/wp/v2/media'

# # 이미지 업로드
# files = {'file': open(image_file_name, 'rb')}
# # Prepare the header of our request
# response = requests.post(media_url, files=files, headers=headers)
# print(response)

# # 업로드된 이미지의 ID 가져오기
# if response.status_code == 201:
#     image_id = response.json()['id']
#     print('이미지가 성공적으로 업로드되었습니다.')
#     print('이미지 ID:', image_id)
# else:
#     print('이미지 업로드에 실패하였습니다.')
#     print(f'\n에러 메시지:', response.text.encode('utf-8').decode('unicode_escape'))
#     exit()

headers = {
    "Authorization": "Bearer %s" % WP_JWT_TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

status = 'publish'  # 즉시발행：publish, 임시저장：draft
slug = '슬러그 내용을 채워주세요'
title = '타이틀을 적어주세요'
content = '본문의 내용이 들어가면 됩니다'
description = '설명부분이 들어가게 됩니다.'

payload = {"status": status,
           "slug": slug,
           "title": title,
           "content": content,
           "date": dt.now().isoformat(),
           "categories": WP_CATEGORY_ID,
           "tags": WP_TAG_ID,
           #    'featured_media': image_id,  # 이미지 ID
           "excerpt": description
           #    "meta": {
           #         "description": "test description",
           #         "keywords": "test keywords",
           #         "filter": "raw"
           #         }
           }

image_id = None  # 이번에는 이미지 업로드를 하지 않을거기 때문에 None 을 입력했습니다.(용량 문제 있을 수 있음 그냥 링크로 가는게 맞을듯)
# 추후에 이미지를 업로드 하게 된다면 업로드 된 이미지의 아이디를 입력하시면 특성이미지로 설정이 됩니다.
if image_id is not None:
    payload['featured_media'] = image_id

try:
    res = requests.post(urljoin(WP_URL, "wp-json/wp/v2/posts"),
                        data=json.dumps(payload),  # python object 를 json으로
                        headers=headers)

    if res.ok:
        print(f"\n성공 code:{res.status_code}")
    else:
        print(
            f"실패 code:{res.status_code} reason:{res.reason} msg:{res.text.encode('utf-8').decode('unicode_escape')}")
except:
    print("UNKNOW ERROR or CONNECTIONTIMEOUT ERROR")
    pass
# requests.exceptions.ConnectTimeout: HTTPSConnectionPool(host='ree31206.mycafe24.com', port=443): Max retries exceeded with url: /wp-json/wp/v2/posts (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x0000028CE63844D0>, 'Connection to ree31206.mycafe24.com timed out. (connect timeout=None)'))