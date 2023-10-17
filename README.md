# WeChatSpider
[微信公众号]火电爬虫项目

# 启动过程
1. 注册一个微信公众号的账号
   ![image](https://github.com/dark-lake/WeChatSpider/assets/48641557/1e79aeed-b0d0-4008-a3af-1f29ac222ff0)
3. 登录该微信公众号
4. 点击图文消息
5. 点击引用
6. ![image](https://github.com/dark-lake/WeChatSpider/assets/48641557/78e5679e-e274-4623-9e53-6f3d9c6a480c)
7. 查找公众号之后点击第一个公众号
8. 此时F12查看网络的包,找到
   ![image](https://github.com/dark-lake/WeChatSpider/assets/48641557/bf1975cc-e503-4041-bc92-4c60246eec5e)
9. 然后复制其中的fakeid替换headers.yaml文件中的fakeid
10. 找到标头中的cookies
    ![image](https://github.com/dark-lake/WeChatSpider/assets/48641557/eb543681-8b91-4b3e-b9e7-fdd6cd762f59)
11. 复制替换掉headers.yaml中的cookie
12. 执行updateShuJuKu.py文件,其中有mysql数据库的配置, 暂时不用动
13. updateShuJuKu.py执行完毕后,执行contentPaQu.py开始爬取具体的数据
14. 爬取完毕就OK了
