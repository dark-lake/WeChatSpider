import requests
import time
import random
import yaml

import pandas as pd

# https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&
# count=5&fakeid=Mzg2MzE4MjMxMA==&type=9&query=&token=1102411154&lang=zh_CN&f=json&ajax=1
# headers解析
with open("headers.yaml", 'rb') as fp:
    config = yaml.load(fp, Loader=yaml.SafeLoader)

print(config)
headers = {
    "Cookie": config['cookie'],
    "User-Agent": config['user-agent']
}

# 请求参数设置
url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
begin = "242"         # begin 为开始页码，0代表第1页，从最新开始抓
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

# 结果文件设置
wechat_spider_json_file = "wechat_spider_data.json"

# 获取当前json文件内容，计算已爬取的页数
# if os.path.exists(wechat_spider_json_file):
#     with open(wechat_spider_json_file, "r") as file:
#         wechat_app_msg_list = json.load(file)
# else:
#     wechat_app_msg_list = []
#
# i = len(wechat_app_msg_list)
i = int(begin)
print("之前已抓取{}页文章,将从下一页开始抓取".format(i))

content_list = []

# 使用while循环获取, 直至抓取完成
while True:
    init = i  * int(count)
    params["begin"] = str(init)

    # 随机等待几秒，避免被微信识别到
    num = random.randint(5,10)
    print("等待"+str(num)+"秒，准备抓取第"+str(i+1)+"页，每页"+str(count)+"篇")
    time.sleep(num)

    # 执行抓取接口
    resp = requests.get(url, headers=headers, params = params, verify=False)

    # 抓取失败，退出
    if resp.json()['base_resp']['ret'] == 200013:
        print("触发微信机制，抓取失败，当前抓取第"+str(i+1)+"页，每页"+str(count)+"篇")
        break

    # 抓取完成，结束
    if len(resp.json()['app_msg_list']) == 0:
        print("已抓取完所有文章，共抓取"+str((i+1)*int(count))+"篇")
        break

    for item in resp.json()["app_msg_list"]:
        # 提取每页文章的标题及对应的url
        items = []
        items.append(item["title"])
        items.append(item["link"])
        content_list.append(items)
    # 抓取成功，json格式保存返回的接口信息
    # wechat_app_msg_list.append(resp.json())
    print("抓取第"+str(i+1)+"页成功，每页"+str(count)+"篇, 共抓取了"+str((i+1)*int(count))+"篇")
    # 循环下一页
    i += 1

name = ['title', 'link']
test = pd.DataFrame(columns=name, data=content_list)
test.to_csv("dainlidashuju.csv", mode='a', encoding='utf-8',header=False)
print("保存成功")
