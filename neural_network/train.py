#coding=utf-8
import pickle
import numpy as np
from input_data import *
#读取钓鱼网站关键字列表（标签为p）
with open('../pick/train_images.pick','rb') as images:
    images=pickle.load(images)

#读取被黑网站关键字列表（标签为d）
with open('../pick/train_labels.pick','rb') as labels:
    labels=pickle.load(labels)


train_labels=[]
train_data=[]
test_labels=[]
test_data=[]
validation_labels=[]
validation_data=[]
for d in xrange(300):
	if d%10 == 0:
		test_data.append(images[d])
		test_labels.append(labels[d])
	else :
		train_data.append(images[d])
		train_labels.append(labels[d])
	if d%10 == 0 :
		validation_data.append(images[d])
		validation_labels.append(labels[d])

print len(test_data),len(train_data),len(validation_data)
print len(test_labels),len(train_labels),len(validation_labels)
datasets=DataSets()


#训练集
train_labels=np.array(train_labels)
train_data=np.array(train_data)
datasets.train=DataSet(train_data, train_labels)
#测试集
test_labels=np.array(test_labels)
test_data=np.array(test_data)
datasets.test=DataSet(test_data, test_labels)
#验证集
validation_labels=np.array(validation_labels)
validation_data=np.array(validation_data)
datasets.validation=DataSet(validation_data, validation_labels)

import bp_nerual_network as nn
nn.train(datasets)
