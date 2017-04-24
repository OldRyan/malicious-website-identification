#coding=utf-8
import sys  
import re
import chardet
import urllib

reload(sys)  
sys.setdefaultencoding("utf-8") 

#索引文件位置
index=open('../file_list.txt','r')

#获取网页URL，标签等信息
#每调用一次读取下一行
def getPageInfo():
    page = index.readline()
    page_info = page.split(',')
    label = page_info[1]
    file_name = page_info[2]
    url = page_info[3]
    return label,file_name,url





#通过文件名从file1目录中获取网页文本内容
def getPageContent(file_name):

    with open('../file1/'+file_name,'r') as html:
        content = html.read()
        char=chardet.detect(content)
        content=content.decode(char['encoding'],'ignore')

        #解码ncr
        content=re.sub(r'\&\#\d{4,6}\;', lambda m: HTMLParser().unescape(m.group(0)), content, 0)

    return content
    '''
    from bs4 import BeautifulSoup
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


    return content,soup
    '''

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


#提取钓鱼网页关键字
def getKeywords(content):
    words = [u'支付',u'账号',u'银行',u'金融',u'信息',u'登录',u'订单',u'交易',u'付款',u'客服',u'输入',u'手机',u'积分',
    u'查询',u'订购',u'缴费',u'查询',u'信用卡',u'业务',u'客户',u'金额',u'特惠',u'优惠',u'姓名',u'身份证',u'规则',u'密码',
    u'账号','ID',u'商品',]
    output=[]
    word_index=0
    for w in words:
        if re.search(w,content):
            output.append(1)
        else: output.append(0)
    return output


#统计网页中文字数
def getTotalChar(content):
    re_words = re.compile(u"[\u4e00-\u9fa5]")
    
    count=[]
    try:
        count = re.findall(re_words, unicode(content))
    except: print 'Count Chinese character error'
    return len(count)        



#统计HTML标签数量
def getHtmlLabels(content):
    countList=[]
    labels=['<title','<link','<a','<img','<href','<span','<div','<font','<input',r'<h\d','<li',]
    for x in labels:
        count=len(re.findall(x,content))
        countList.append(count)
    return countList

'''
s1=getPageContent('f51fb0c9073196c8426d318387b2bd59')
print getKeywords(s1)
'''
for x in xrange(1,100):
    try:
        passlabel,file_name,url=getPageInfo()
        print file_name

        s1=getPageContent(file_name)
        print extractRequestRealm(s1,url)
        print getTotalChar(s1)
        print getKeywords(s1)
        print getHtmlLabels(s1)

    except: pass  
