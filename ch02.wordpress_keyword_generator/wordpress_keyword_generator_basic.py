import requests
from pprint import pprint as pp

headers = {
    'referer': 'https://itemscout.io/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

data = {
    'duration': '30d',
    'genders': 'f,m',
    'ages': '10,60',
}

response = requests.post('https://api.itemscout.io/api/category/1301/data', headers=headers, data=data, verify=False).json()

# pp(response)

# pp(response['data']['data'])

for idx, item in enumerate(response['data']['data'].items()):
    print(f"{idx + 1}. ID {item[0]} | keyword {item[1]['keyword']}")