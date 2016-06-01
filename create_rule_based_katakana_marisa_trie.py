# coding: utf-8
import codecs

import marisa_trie

"""
Used to create marisa-trie for Kaji et al's paraphrase-based features
"""

infile = codecs.open('/Users/Fujinuma/Projects/transliteration/katakanaRuleBasedTrainingExamplesWithSpace.txt', 'r', 'utf-8')

rulebased_katakana_trie = {}

for line in infile:
    columns = line[:-1].split('\t')

    if len(columns) == 2:
        # print columns[0]
        if columns[0] in rulebased_katakana_trie:
            rulebased_katakana_trie[columns[0]] += int(columns[1])
        else:
            rulebased_katakana_trie[columns[0]] = int(columns[1])

rulebased_katakana_trie_marisa = marisa_trie.RecordTrie(str("<i"), map(lambda (x, y):(x, [y]), rulebased_katakana_trie.items()))
#tf_trie_marisa.save('my_trie_copy.marisa')
import pickle
f = open('rule_based_katakana_training.txt','wb')
pickle.dump(rulebased_katakana_trie_marisa, f)