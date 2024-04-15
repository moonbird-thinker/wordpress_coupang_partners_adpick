# # 필요한 패키지들을 리스트에 저장합니다.
# import subprocess
# packages = [
#     "python-wordpress-xmlrpc",
# ]
#
# # 각 패키지를 설치합니다.
# for package in packages:
#     try:
#         # pip를 통해 패키지를 설치합니다.
#         subprocess.check_call(["pip", "install", package])
#         print(f"{package} installed successfully!")
#     except subprocess.CalledProcessError:
#         # 패키지 설치 실패 메시지 출력
#         print(f"Failed to install {package}.")
#     # 설치가 완료되었으면 코드블럭 아래에 설치 완료 메시지를 출력합니다.
#     print("\nAll packages installed successfully!")

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
import collections
from _collections_abc import Iterable
collections.Iterable = Iterable

# url, username, password
wordpress_address = 'http://워드프레스주소/xmlrpc.php'
wordpress_id = ''
wordpress_pw = ''

client = Client(wordpress_address, wordpress_id, wordpress_pw)
# client = Client("워드프레스주소/xmlrpc.php", "워드프레스 아이디", "워드프레스비밀번호")

post = WordPressPost()

post.title = 'HTML5 - Intoduction'

# HTML content
content = """<!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
</head>
<body>

<h2>HTML Table</h2>

<table>
  <tr>
    <th>Company</th>
    <th>Contact</th>
    <th>Country</th>
  </tr>
  <tr>
    <td>Alfreds Futterkiste</td>
    <td>Maria Anders</td>
    <td>Germany</td>
  </tr>
  <tr>
    <td>Centro comercial Moctezuma</td>
    <td>Francisco Chang</td>
    <td>Mexico</td>
  </tr>
  <tr>
    <td>Ernst Handel</td>
    <td>Roland Mendel</td>
    <td>Austria</td>
  </tr>
  <tr>
    <td>Island Trading</td>
    <td>Helen Bennett</td>
    <td>UK</td>
  </tr>
  <tr>
    <td>Laughing Bacchus Winecellars</td>
    <td>Yoshi Tannamuri</td>
    <td>Canada</td>
  </tr>
  <tr>
    <td>Magazzini Alimentari Riuniti</td>
    <td>Giovanni Rovelli</td>
    <td>Italy</td>
  </tr>
</table>

</body>
</html>
"""

post.content = content
post.mime_type = "text/html"

post.terms_names = {
  'post_tag': ['tag1', 'tag2'],
  'category': ['category1', 'category2']
}
post.post_status = "publish"
try:
    post_id = client.call(posts.NewPost(post))
    if post_id:
        print('포스팅 완료')
        print("Post with id (", post_id, ") successfully published")
except ():
    print('포스팅 실패')

# Getting list of posts
published_posts = client.call(posts.GetPosts({'post_status': 'publish'}))
print(published_posts)
