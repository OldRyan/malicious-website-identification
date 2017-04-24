#coding=utf-8
from feature_extract import *

#对定量特征进行二值化

#统计三类站点的字数
p_Char=[]
d_Char=[]
n_Char=[]
#统计请求数
p_reqIn=[]
p_reqOut=[]
d_reqIn=[]
d_reqOut=[]
n_reqIn=[]
n_reqOut=[]
#统计标签数量
p_labels=[]
d_labels=[]
n_labels=[]

for i in xrange(40000):
	label,file_name,url = getPageInfo(i-1)
	#钓鱼站点
	if label == 'p':
		content = getPageContent(file_name)
		count = content.getTotalChar()
		#字数统计
		p_Char.append(count)
		req=extractRequestRealm(content,url)
		#域名请求
		p_reqIn.append(req[0])
		#跨域请求
		p_reqOut.append(req[1])
		#标签数量
		label=getHtmlLabels(content)
		p_labels.append(label)


	#被黑站点
	elif label == 'd':
		content = getPageContent(file_name)
		count = content.getTotalChar()
		d_Char.append(count)
		req=extractRequestRealm(content,url)
		d_reqIn.append(req[0])
		d_reqOut.append(req[1])
		label=getHtmlLabels(content)
		q_labels.append(label)	
	#正常站点
	else :
		content = getPageContent(file_name)
		count = content.getTotalChar()
		n_Char.append(count)
		req=extractRequestRealm(content,url)
		n_reqIn.append(req[0])
		n_reqOut.append(req[1])
		label=getHtmlLabels(content)
		n_labels.append(label)
