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
    #第一种形式:http://开头
    re_outside_realm1 = re.compile(r'[\'|\"]http[s]*\:\/\/[\-|\d|\w|\/|\.]+[\'|\"]')
    #第二种形式://开头
    re_outside_realm2 = re.compile(r'[\'|\"][\/]{2}[\d|\w||\/|\-]+\.\w{1,5}')
    outside_requests = re.findall(re_outside_realm1,content)
    outside_requests.extend(re.findall(re_outside_realm2,content))
    #从url中提取域名
    
    domain=re.search(r'[www.]*[\d|\w|\.|\-]+\/',url).group(0).split('.')[-2]
    #去除域内请求
    inside=0
    for x in outside_requests:
        if re.search(domain,x):
            inside=inside+1
    
    #域内资源请求：
    re_inside_realm = re.compile(r'[\'|\"][\/]{0,1}[^\/][\w|\/|\-]+\.\w{1,5}')
    inside_requests = re.findall(re_inside_realm,content)
    #返回列表：[域外，域内]
    return [len(outside_requests)-inside,len(inside_requests)+inside]

'''
def extractIPC(content):
    if re.search('ICP',content):
        ICP=re.search(r'.*ICP.*',content).group(0)
        print ICP
        ICP=re.search(r'\d{8}',ICP)
        print ICP.group(0)
'''

#提取钓鱼网页关键字
def getKeywords(content1,content2):
    words = ['支付','账号','银行','金融','信息','登录','订单','交易','付款','客服','输入','手机','积分',
    '查询','订购','缴费','查询','信用卡','业务','客户','金额','特惠','优惠','姓名','身份证','规则','密码',
    '账号','ID','商品',]
    output=[]
    word_index=0
    for w in words:
        if re.search(w,content1) or re.search(w,content2):
            output.append(1)
        else: output.append(0)
    return output


#统计网页中文字数
def getTotalChar(content1,content2):
    re_words = re.compile(u"[\u4e00-\u9fa5]")
    try:
        len1='0'
        len2='0'
        try:
            len1 = re.findall(re_words, unicode(content1))
        except:pass
        try:
            len2 = re.findall(re_words, unicode(content2))
        except Exception,e: pass



        if len(len1)>len(len2):
            return len(len1)
        else : return len(len2)
    except Exception,e: return 0
def isError(content1,content2):
    pass

'''
s1,s2=getPageContent('6a4effb7f61acf2f4cc1932fb313ca03')
print extractRequestRealm(s1,'http://www.fyygcw.com/xz/html/pid-01010414/id-38942.html')
print getTotalChar(s1,s2)
'''
for x in xrange(1,100):
    try:
        passlabel,file_name,url=getPageInfo()
        print file_name

        s1,s2=getPageContent(file_name)
        #print extractRequestRealm(s1,url)
        print getTotalChar(s1,s2)

    except: pass  
