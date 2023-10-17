import numpy as np
import pandas as pd

import pymysql
import csv

with open('output.csv', 'r',encoding='utf-8') as f:
    data=[tuple(line) for line in csv.reader(f)]

conn = pymysql.connect(
    host='39.96.138.111',
    port=3306,
    user='root',
    password='root',
    charset='utf8',
    autocommit=True)
conn.select_db("myReptile")

sql_1 = 'insert into reptile_data(rep_name,rep_link,rep_content) values(%s,%s,null)'  # 注意，这里的%s不需要加引号，使用execute需要加引号。另外，executemany 在执行过程中能够将python的None转为sql的null，这一点挺方便的

cursor = conn.cursor()
cursor.executemany(sql_1, data[1:])
conn.commit()
cursor.close()
conn.close()