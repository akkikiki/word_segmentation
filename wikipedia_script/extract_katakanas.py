# coding: utf-8
import codecs
import re
from hat_trie import Trie

dic = Trie()

pattern = re.compile(u"[\u30A0-\u30FA\u30FC-\u30FF]+", re.UNICODE)

f_wikipedia = codecs.open('../data/test_data/uniq_katakanas.txt_perceptron_tfisf_bigram_eta0.1', 'r', 'utf-8')
f_out = codecs.open('katakana_occurrences_python.txt', 'w', 'utf-8')

for line in f_wikipedia:
    groups = re.findall(pattern, line)
    for group in groups:
        if group in dic:
            dic[group] += 1
        else:
            dic[group] = 1

for key in dic.keys():
    f_out.write("%s\t%d\n" % (key, dic[key]))