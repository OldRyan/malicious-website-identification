#coding=utf-8
import sys  
import re
from bs4 import BeautifulSoup
import urllib

reload(sys)  
sys.setdefaultencoding("utf-8") 

f=open('../file_list.txt','r')

#获取网页URL，标签等信息
def getPageInfo():
    page = f.readline()
    page_info = page.split(',')
    label = page_info[1]
    file_name = page_info[2]
    url = page_info[3]
    return label,file_name,url





#通过文件名从file1目录中获取网页文本内容
#由于解码问题，返回两种网页文本，提高解码成功的概率
def getPageContent(file_name):
    soup = BeautifulSoup(open("../file1/"+file_name), "html.parser")
    soup=str(soup)

    
    with open('../file1/'+file_name,'r') as html:
        
        content = html.read()

        #gbk编码转换
        if re.search(r'charset=gbk',content,re.I):
            content=content.decode('gbk','ignore')

        elif re.search(r'charset=gb2312',content,re.I):
            content=content.decode('gb2312','ignore')


        #print soup
        #解码ncr
        content=re.sub(r'\&\#\d{4,6}\;', lambda m: HTMLParser().unescape(m.group(0)), content, 0)
        


    re_words = re.compile(u"[\u4e00-\u9fa5]+")

    ''' 
    s=unicode(soup)
    len_soup = re.findall(re_words, s)
    s=unicode(content)
    len_content =  re.findall(re_words, content)
    for s in  len_soup:
        print s
    '''
    return content,soup


#提取请求域特征，
#返回跨域请求数和域内请求数
def extractRequestRealm(content,url):
    #域外资源请求
    re_outside_realm = re.compile(r'[\'|\"]http[s]*\:\/\/[\d|\w||\/]+\.\w{1,5}')
    outside_requests = re.findall(re_outside_realm,content)
    #域内资源请求
    re_inside_realm = re.compile(r'[\'|\"][^\/][\d|\w||\/]+\.\w{1,5}')
    inside_requests = re.findall(re_inside_realm,content)
    return [len(outside_requests),len(inside_requests)]

s1,s2=getPageContent('b242d4d926ce8fb4990c930736da74c5')
print extractRequestRealm(s1,'a')
