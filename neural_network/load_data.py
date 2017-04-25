#coding=utf-8
import pickle
#读取钓鱼网站关键字列表（标签为p）
with open('../pick/train_images.pick','rb') as images:
    images=pickle.load(images)

#读取被黑网站关键字列表（标签为d）
with open('../pick/train_labels.pick','rb') as labels:
    labels=pickle.load(labels)

print images[3],labels[3]