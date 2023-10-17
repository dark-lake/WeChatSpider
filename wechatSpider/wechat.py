import wechatsogou

# 可配置参数

# 直连
from wechatsogou import WechatSogouAPI

def get_gzh_article(name):
    """
    功能: 查找指定公众号的文章
    :param name:文章关键字
    :return:
    """
    wechats = WechatSogouAPI(captcha_break_time=1)
    data = wechats.get_gzh_article_by_history(name)
    print(data)

get_gzh_article("电力案例大数据")