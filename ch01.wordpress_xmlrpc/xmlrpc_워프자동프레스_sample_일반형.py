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

# url, username, password
wordpress_address = 'http://워드프레스주소/xmlrpc.php'
wordpress_id = ''
wordpress_pw = ''

# wordpress 포스팅 - Rename XMLRPC 플러그인
client = Client(wordpress_address, wordpress_id, wordpress_pw)
# client = Client("워드프레스주소/xmlrpc.php", "워드프레스 아이디", "워드프레스비밀번호")
postx = WordPressPost()
postx.title = "글제목입니다."
postx.slug = "글제목슬러그"
postx.content = "글내용입니다."
postx.terms_names = {
    'post_tag': 'tag1'
    , 'category': ['category1']  # category 안쓰면 500 error
}
postx.post_status = 'publish'  # publish: 바로 발행 // draft: 임시저장
# client.call(posts.NewPost(postx))
try:
    ret = client.call(posts.NewPost(postx))
    if ret:
        print('포스팅 완료')
except():
    print('포스팅 실패')