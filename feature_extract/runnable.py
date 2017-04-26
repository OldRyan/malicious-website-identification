#coding=utf-8
from feature_extract import *
images=[]
labels=[]
for i in xrange(39999):
	print i
	image=[]
	label,file_name,url = getPageInfo(i)
	#读取网页
	content = getPageContent(file_name)
	#字数统计
	count = getTotalChar(content)
	#字数为0可能解析失败，使用soup
	if count==0:
		content = getPageContent_soup(file_name)
		count = getTotalChar(content)
	#*************************
	#特征F1:[汉字数量/10000]
	if count>10000:
		image.append(1)
	else : image.append(count/10000.0)
	#*************************
	#特征F2:[域外请求/总请求]
	req=extractRequestRealm(content,url)
	image.append(req[0]/(req[0]+req[1]+1.0))
	#*************************
	#特征F3:[HTML标签数量]
	htmlLabels = getHtmlLabels(content)
	#link标签
	if htmlLabels[0]>30:
		image.append(1)
	else : image.append(htmlLabels[0]/30.0)
	#a标签
	if htmlLabels[1]>300:
		image.append(1)
	else : image.append(htmlLabels[1]/300.0)
	#img标签
	if htmlLabels[2]>100:
		image.append(1)
	else : image.append(htmlLabels[2]/100.0)
	#span标签
	if htmlLabels[3]>500:
		image.append(1)
	else : image.append(htmlLabels[3]/500.0)
	#div标签
	if htmlLabels[4]>500:
		image.append(1)
	else : image.append(htmlLabels[4]/500.0)
	#font标签
	if htmlLabels[5]>50:
		image.append(1)
	else : image.append(htmlLabels[5]/50.0)
	#input标签
	if htmlLabels[6]>30:
		image.append(1)
	else : image.append(htmlLabels[6]/30.0)
	#h标签
	if htmlLabels[7]>100:
		image.append(1)
	else : image.append(htmlLabels[7]/100.0)
	#li标签
	if htmlLabels[8]>300:
		image.append(1)
	else : image.append(htmlLabels[8]/300.0)
	#*************************
	#提取特征F4:[关键字]
	key = findKeywords(content)
	image.extend(key)
	#*************************
	images.append(image)
	if label=='n':
		labels.append([1,0,0])
	elif label=='p' :
		labels.append([0,1,0])
	elif label=='d' : 
		labels.append([0,0,1])
	else :print label,file_name
	if (i+1)%50 == 0 :
		with open('../pick/train_images-'+str(i/50)+'.pick','wb') as f1:
			pickle.dump(images,f1)
		with open('../pick/train_labels-'+str(i/50)+'.pick','wb') as f2:
			pickle.dump(labels,f2)
		print 'Data Saved, i = '+str(i)
		images=[]
		labels=[]

with open('../pick/train_images.pick-n','wb') as f1:
	pickle.dump(images,f1)
with open('../pick/train_labels.pick-n','wb') as f2:
	pickle.dump(labels,f2)

