import requests
from bs4 import BeautifulSoup
import pymysql as my

img_list = []
style_list = ['모던', '북유럽', '빈티지', '내추럴', '프로방스&로맨틱', '클래식&앤틱', '한국&아시아', '유니크']

for i in range(len(style_list)):
    page = requests.get('https://ohou.se/contents/card_collections?style=' + str(i))
    soup = BeautifulSoup(page.content, 'html.parser')

    # 이미지 링크
    img = soup.find_all('img')
    for x in range(2, 50, 2):
        img_list.append(img[x].get('src'))

    # db 연결스트림 만들기
    con = my.connect(host='localhost', port=3708, user='root', password='1234', db='todayhouse')
    cursor = con.cursor()

    for j in range(len(img_list)):
        sql = "insert into images values (%s, %s)"
        result = cursor.execute(sql, (img_list[j], style_list[i]))

    img_list = []

    con.commit()
    con.close()
