import requests
from bs4 import BeautifulSoup
import pymysql as my

# 수납정리 11, 생활용품 4, 주방 5, 셀프시공 6, 시공/서비스 7, 반려동물 8
category_num = [11, 4, 5, 6, 7, 8, ]

# id : auto
name_list = []
# category
price_list = []
brand_list = []
photo_list = []
discount_list = []
# keyword

page = requests.get('https://ohou.se/store/category?affect_type=StoreHamburger&category=11')
soup = BeautifulSoup(page.content, 'html.parser')
name = soup.select('div')
print(name)
for x in name:
    print(x)

# for i in category_num:
#     page = requests.get('https://ohou.se/store/category?affect_type=StoreHamburger&category=' + str(i))
#     soup = BeautifulSoup(page.content, 'html.parser')

