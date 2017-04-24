#coding=utf-8
from feature_extract import *

p_keyword=[]
d_keyword=[]
#遍历训练集，提取其中钓鱼网站的关键词
for i in range(1000):
    
    label,file_name,url = getPageInfo(i-1)
    if label == 'p':
        content = getPageContent(file_name)
        word = getKeywords(content,5)

        for w in word:
            if w not in p_keyword:
                p_keyword.append(w)
                print w

    if label == 'd':
        content = getPageContent(file_name)
        word = getKeywords(content,8)

        for w in word:
            if w not in d_keyword:
                d_keyword.append(w)
                print w    

import pickle

f=open('p_keyword.pick','wb')
pickle.dump(p_keyword,f)
f.close()
print "P keyword saved on p_keyword.pick"

f=open('d_keyword.pick','wb')
pickle.dump(d_keyword,f)
f.close()
print "D keyword saved on d_keyword.pick"