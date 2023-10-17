import jieba
import pymysql
import re

conn = pymysql.connect(
    host='39.96.138.111',
    port=3306,
    user='root',
    password='root',
    charset='utf8',
    autocommit=True)
conn.select_db("myReptile")
cursor = conn.cursor()

def dianLiAnLiDaShuJu(str):
    start = str.find("正文：")
    if start!=-1:
        str=str[start+3:]
    end = str.rfind("亲身经历过小大事故")
    if end!= -1:
        str = str[:end]
    return str

#获取停用词 列表
def get_stopwords():
# 去除停用词之后再提取关键词
    stopword=[line.strip() for line in open('./all_stopword.txt',encoding='utf-8').readlines()]
    return stopword

def _word_ngrams(tokens, stop_words,ngram_range=(2,2)):
    #处理停用词
    if stop_words is not None:
        tokens=[w for w in tokens if w not in stop_words and len(w)<3]
    #处理N-grams
    min_n,max_n=ngram_range
    if max_n!=1:
        original_tokens=tokens
        tokens=[]
        n_original_tokens=len(original_tokens)
        for n in jieba.xrange(min_n, min(max_n + 1, n_original_tokens + 1)):
            for i in jieba.xrange(n_original_tokens - n + 1):
                tokens.append(''.join(original_tokens[i:i+n]))
    return tokens

#分词
def seg(text):
    pattern = r'、|，|。|\s|；|\n|\t|,|[0-9A-Za-z]|-'
    result = re.split(pattern, text)
    content = ' '.join(result)  # 去除文本中异常的字符、英文、数字
    cut = jieba.cut(content)
    list_cut = list(cut)  # 将结果转化为列表形式
    # 除列表中的\n
    listcut = [x.strip() for x in list_cut]
    # print(listcut)
    return listcut

cursor.execute("SELECT rep_id,rep_content FROM reptile_data LIMIT 7 offset 0")
reptileList = cursor.fetchall()
for reptile in reptileList:
    text = dianLiAnLiDaShuJu(reptile[1])
    print(text)
    # n_gramwords = _word_ngrams(seg(text), get_stopwords(), ngram_range=(2, 2))
    # print(n_gramwords)
    # # print(reptile[0],reptile[1])
    # ciList = jieba.cut_for_search(dianLiAnLiDaShuJu(reptile[1]))
    # for ci in ciList:
    #     print(ci)