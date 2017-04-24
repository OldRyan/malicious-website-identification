import chardet
import urllib
f=open('../file1/b242d4d926ce8fb4990c930736da74c5','r')
t=f.read()
cha=chardet.detect(t)
print t.decode(cha['encoding'],'ignore')