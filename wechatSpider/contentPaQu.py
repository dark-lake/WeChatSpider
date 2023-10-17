import time
import random

import pymysql
import requests
from bs4 import BeautifulSoup
import re
import urllib3
from pymysql.converters import escape_string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conn = pymysql.connect(
    host='39.107.248.250',
    port=3306,
    user='root',
    password='Sigsit123',
    charset='utf8',
    autocommit=True)
conn.select_db("myReptile")
cursor = conn.cursor()



def filter_emoji(desstr, restr=''):
    # 过滤表情
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def get_html(url):
    # 创建一个响应对象
    response=requests.get(url)
    # 获取整个网页的HTML内容
    html_page=response.text
    content = BeautifulSoup(html_page, 'lxml').get_text()
    # 返回网页的HTML内容
    return content.replace(" ", "").replace("\n", "")

cursor.execute("select count(*) as start_id from reptile_data where rep_content is not NULL; ")
start_id = cursor.fetchone()[0] # result is a tuple (start_id,) the start_id is the first one that rep_content is null
print(f'上次更新到了{start_id}位置')
cursor.execute("select count(*) as end_id from reptile_data where rep_content is null;")
need_num = cursor.fetchone()[0]
print(need_num)
cursor.execute("SELECT rep_link FROM reptile_data LIMIT "+ str(need_num) +" offset "+str(start_id)+";")
# cursor.execute("SELECT rep_link FROM reptile_data")
linkList = cursor.fetchall()
# with open('all.txt','w') as f:
#     for i in linkList:
#         f.writelines(i)
# print(linkList)


for link in linkList:
    print(link)
    num = random.randint(4, 6)
    time.sleep(num)
    print(get_html(link[0]))
    cursor.execute("update reptile_data set rep_content = '"+escape_string(filter_emoji(get_html(link[0])))+"' where rep_link='"+link[0]+"'")
