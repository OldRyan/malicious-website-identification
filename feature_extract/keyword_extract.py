#coding=utf-8
from feature_extract import *

p_keyword=[]
d_keyword=[]
#遍历训练集，提取其中钓鱼网站的关键词
#训练集中共39999条数据
for i in xrange(39999):
    #获取第i行的标签，文件名，URL
    label,file_name,url = getPageInfo(i)
    #如果标签为p，钓鱼页面
    if label == 'p':
        #获取网页源代码
        content = getPageContent(file_name)
        #提取源代码中的关键字
        word = getKeywords(content,5)
        #如果当前提取到的不在关键字列表中则加入列表
        for w in word:
            if w not in p_keyword:
                p_keyword.append(w)

    #如果标签为d，被黑页面
    if label == 'd':
        content = getPageContent(file_name)
        word = getKeywords(content,5)
  
        for w in word:
            if w not in d_keyword:
                d_keyword.append(w)
                print w    

#pickle用于序列化列表
import pickle
#保存p类关键字
f=open('../pick/p_keyword.pick','wb')
pickle.dump(p_keyword,f)
f.close()
print "P keyword saved on p_keyword.pick"
#保存d类关键字
f=open('../pick/d_keyword.pick','wb')
pickle.dump(d_keyword,f)
f.close()
print "D keyword saved on d_keyword.pick"