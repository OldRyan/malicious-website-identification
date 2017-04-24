import sys
sys.path.append('../')

import jieba
import jieba.analyse
from optparse import OptionParser
'''
USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

parser = OptionParser(USAGE)
parser.add_option("-k", dest="topK")
opt, args = parser.parse_args()


if len(args) < 1:
    print(USAGE)
    sys.exit(1)

file_name = args[0]

if opt.topK is None:
    topK = 10
else:
    topK = int(opt.topK)
'''
content = open('../file1/ebe9801e104b262666716439c668793b', 'rb').read()

tags = jieba.analyse.extract_tags(content, topK=3)

print(",".join(tags))
