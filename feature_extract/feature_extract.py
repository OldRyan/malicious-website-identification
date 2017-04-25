#coding=utf-8
import sys  
import re
import chardet
import urllib
import jieba
import jieba.analyse
from HTMLParser import HTMLParser
from bs4 import BeautifulSoup

#设置系统编码为UTF-8
reload(sys)  
sys.setdefaultencoding("utf-8") 

#打开索引文件
index=open('../file_list.txt','r')
#按行读取整个文件
pages=index.readlines()

#获取网页URL，标签等信息
#输入参数为行数
def getPageInfo(num):
    #获得参数对应行
    page = pages[num]
    #分割字符串
    page_info = page.split(',')
    label = page_info[1]
    file_name = page_info[2]
    url = page_info[3]
    return label,file_name,url

#通过文件名从file1目录中获取网页文本内容
def getPageContent(file_name):

    with open('../file/'+file_name,'rb') as html:
        #读取网页源代码
        content = html.read()
        #侦测源代码编码
        char=chardet.detect(content)
        #读取编码或网页文件出错时
        if content==None or char['encoding']== None:
            return ""
        #统一解码成utf8
        content=content.decode(char['encoding'],'ignore')

        #解码NCR
        content=re.sub(r'\&\#\d{4,6}\;', lambda m: HTMLParser().unescape(m.group(0)), content, 0)

    return content

#使用BeautifulSoup解析网页
def getPageContent_soup(file_name):
    soup = BeautifulSoup(open("../file/"+file_name), "html.parser")
    soup = str(soup)
    return soup


#提取请求域特征，
#返回跨域请求数和域内请求数
def extractRequestRealm(content,url):
    #域外资源请求
    #第一种形式:http://开头可能是域外请求
    re_outside_realm1 = re.compile(r'[\'|\"]http[s]*\:\/\/[\-|\d|\w|\/|\.]+[\'|\"]')
    #第二种形式://开头可能是域外请求
    re_outside_realm2 = re.compile(r'[\'|\"][\/]{2}[\d|\w||\/|\-]+\.\w{1,5}')
    outside_requests = re.findall(re_outside_realm1,content)
    #合并前两种形式
    outside_requests.extend(re.findall(re_outside_realm2,content))
    #从url中提取网站域名
    try:
        domain=re.search(r'[www.]*[\d|\w|\.|\-]+\/',url).group(0).split('.')[-2]
        #在第一种形式的请求中包含站点域名则是域内请求
        #找出前两种形式中是域内请求的数量
        inside=0
        for x in outside_requests:
            if re.search(domain,x):
                inside=inside+1
    except:inside=0
    #以目录索引形式访问资源一定是域内请求
    re_inside_realm = re.compile(r'[\'|\"][\/]{0,1}[^\/][\w|\/|\-]+\.\w{1,5}')
    inside_requests = re.findall(re_inside_realm,content)
    #返回列表：[域外，域内]
    return [len(outside_requests)-inside,len(inside_requests)+inside]

import pickle
#读取钓鱼网站关键字列表（标签为p）
with open('../pick/p_keyword.pick','rb') as p_keyword_pick:
    p_keyword=pickle.load(p_keyword_pick)

#读取被黑网站关键字列表（标签为d）
with open('../pick/d_keyword.pick','rb') as d_keyword_pick:
    d_keyword=pickle.load(d_keyword_pick)

#从网页中匹配可疑关键字
def findKeywords(content):

    output=[]
    #查找钓鱼网站关键字
    for w in p_keyword:
        if re.search(w,content):
            output.append(1)
        else: output.append(0)
    #查找被黑页面关键字
    for w in d_keyword:
        if re.search(w,content):
            output.append(1)
        else: output.append(0)    
    return output


#统计网页中文字数
def getTotalChar(content):
    #所有汉字的unicode编码
    re_words = re.compile(u"[\u4e00-\u9fa5]")
    
    count=[]
    try:
        #匹配出网页中的汉字
        count = re.findall(re_words, unicode(content))
    except: print 'Count Chinese character error'
    #返回汉字的数量
    return len(count)        

#获取网页中的中文关键字
def getKeywords(content,topK=3):
    re_words = re.compile(u"[\u4e00-\u9fa5]")
    
    try:
        char = re.findall(re_words, unicode(content))
    except: print 'Get Chinese character error'
    #合并所有汉字后提取关键字，默认提取3个关键字
    tags = jieba.analyse.extract_tags("".join(char), topK)
    return tags


#统计HTML标签数量
def getHtmlLabels(content):
    countList=[]
    #常用html标签
    labels=['<link','<a','<img','<span','<div','<font','<input',r'<h\d','<li',]
    for x in labels:
        count=len(re.findall(x,content))
        countList.append(count)
    return countList

'''
a,b,c=getPageInfo(487)
print getPageContent_soup(b)
'''