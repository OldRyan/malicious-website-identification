import pickle



with open('../pick/train_images-0.pick','rb') as f0:
    d0=pickle.load(f0)


with open('../pick/train_images-1.pick','rb') as f1:
    d1=pickle.load(f1)

with open('../pick/train_images-2.pick','rb') as f2:
    d2=pickle.load(f2)

print len(d0),len(d2)