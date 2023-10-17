import pymysql
import requests
import time
import random
import yaml
import urllib3

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

# headers解析
with open("headers.yaml", 'rb') as fp:
    config = yaml.load(fp, Loader=yaml.SafeLoader)

headers = {
    "Cookie": config['cookie'],
    "User-Agent": config['user-agent']
}

# 请求参数设置
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
begin = "0"         # begin 为开始页码，0代表第1页，从最新开始抓
count = "5"         # count 为每页获取的文章个数
params = {
    "action": "list_ex",
    "begin": begin,
    "count": count,
    "fakeid": config['fakeid'],
    "type": "9",
    "token": config['token'],
    "lang": "zh_CN",
    "f": "json",
    "ajax": "1"
}

i = int(begin)
print("开始抓取")


# 使用while循环获取, 直至抓取完成
while True:
    init = i  * int(count)
    params["begin"] = str(init)

    # 随机等待几秒，避免被微信识别到
    # num = random.randint(5,10)
    num = random.randint(3, 7)
    print("等待"+str(num)+"秒，准备抓取第"+str(i+1)+"页，每页"+str(count)+"篇")
    time.sleep(num)

    # 执行抓取接口
    resp = requests.get(url, headers=headers, params = params, verify=False)
    print(resp.json())
    # 抓取失败，退出
    if resp.json()['base_resp']['ret'] == 200013:
        print("触发微信机制，抓取失败，当前抓取第"+str(i+1)+"页，每页"+str(count)+"篇")
        break

    # 抓取完成，结束
    if len(resp.json()['app_msg_list']) == 0:
        print("已抓取完所有文章，共抓取"+str((i+1)*int(count))+"篇")
        break

    # 二维数组,里面每个列表存的是title和link
    content_list = []
    for item in resp.json()["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        content_list.append(items)
    zhuaWanLe = True
    for item in content_list:
        cursor.execute("SELECT rep_name FROM reptile_data WHERE rep_name LIKE '"+item[0]+"'")
        if len(cursor.fetchall())==0:
            zhuaWanLe = False
            print("插入文章："+item[0])
            cursor.execute("insert into reptile_data(rep_name,rep_link,rep_content) values('"+item[0]+"','"+item[1]+"',null)")

    if zhuaWanLe == True:
        print("遇到相同的，抓完了")
        break
    # 抓取成功，json格式保存返回的接口信息
    # wechat_app_msg_list.append(resp.json())
    print("抓取第"+str(i+1)+"页成功，每页"+str(count)+"篇, 共抓取了"+str((i+1)*int(count))+"篇")
    # 循环下一页
    i += 1

print("保存成功")
