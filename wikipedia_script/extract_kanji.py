# coding: utf-8

""" ref;
CJK Unified Ideographs: \u4E00 to \u9FFF
CJK Unified Ideographs Extension A: \u3400 to \u4DFF
CJK Unified Ideographs Extension B: \u20000 to \u2A6DF
CJK Compatibility Ideographs: \uF900 to \uFAFF
CJK Compatibility Ideographs Supplement: \u2F800 to \u2FA1F
"""
import codecs
import re
from hat_trie import Trie

dic = Trie()

# pattern = re.compile(ur"[々〇〻\u3400-\u9FFF\uF900-\uFAFF\U00020000-\U0002a6df]+", re.UNICODE)
pattern = re.compile(ur"[々〇〻\u3400-\u9FFF\uF900-\uFAFF]+", re.UNICODE)


groups = re.findall(pattern, u"龍之介|5=2014年3月12日")
# groups = re.findall(pattern, u"﨟瓊")

for group in groups:
    print group


f_wikipedia = codecs.open('../data/wikipedia/jawiki-20160203-pages-articles.xml', 'r', 'utf-8')
f_out = codecs.open('kanji_occurrences_python.txt', 'w', 'utf-8')

n = 0

for line in f_wikipedia:
    groups = re.findall(pattern, line)
    n += 1
    for group in groups:
        if group in dic:
            dic[group] += 1
        else:
            dic[group] = 1

    if n % 100000 == 0:
        print "finished %d lines" % n

    if n == 10000000:
        # testing purpose
        break

for key in dic.keys():
    f_out.write("%s\t%d\n" % (key, dic[key]))
