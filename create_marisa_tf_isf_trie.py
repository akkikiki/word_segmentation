# coding: utf-8

import marisa_trie
import codecs
import pickle

"""
Input: a file with the number of occurrences of consecutive katakana characters
CAUTION: Running this script will use around 2G of memory.
"""

def extract_all_possible_substrings(word): 
    #substrings = []
    substrings = set()
    for i in range(len(word)):
        for j in range(i+1, len(word) + 1):
            #substrings.append(word[i:j])
            substrings.add(word[i:j])
    return substrings


# infile = codecs.open('data/tfisf/katakanaWordsOccurrence.txt', 'r', 'utf-8')
infile = codecs.open('data/tfisf/katakanaWordsOccurrence_20151226.txt', 'r', 'utf-8')

isf_trie = {} # inverse substring frequency
tf_trie = {} # term frequency
total = 0
for line in infile:
    columns = line[:-1].split('\t')
    if len(columns) == 2:
        total += int(columns[1])
        if columns[0] in tf_trie:
            tf_trie[columns[0]] += int(columns[1])
        else:
            tf_trie[columns[0]] = int(columns[1])
    else:
        if columns[0] in tf_trie:
            tf_trie[columns[0]] += 1
        else:
            tf_trie[columns[0]] = 1


    substrings = extract_all_possible_substrings(columns[0])
    for substring in substrings:
        if substring in isf_trie:
            isf_trie[substring] += 1
        else:
            isf_trie[substring] = 1

print "---isf-trie---"
#for word in isf_trie.keys():
#    print word, str(isf_trie[word])
print "entries: " + str(len(isf_trie.keys()))

print "---tf-trie---"
#for word in tf_trie.keys():
#    print word, str(tf_trie[word])
print "entries: " + str(len(tf_trie.keys()))

#tf_trie.save()
tf_trie_marisa = marisa_trie.RecordTrie(str("<i"), map(lambda (x, y):(x, [y]), tf_trie.items()))
#tf_trie_marisa.save('my_trie_copy.marisa')
# f = open('tf_trie.txt','wb')
f = open('data/tfisf/tf_trie_20151226.txt','wb')
pickle.dump(tf_trie_marisa, f)


isf_trie_marisa = marisa_trie.RecordTrie(str("<i"), map(lambda (x, y):(x, [y]), isf_trie.items()))
# f_isf = open('isf_trie.txt','wb')
f_isf = open('data/tfisf/isf_trie_20151226.txt','wb')
pickle.dump(isf_trie_marisa, f_isf)
#
# word = u'MARIO_IS_MISSING!'
# #word = u"ワイン"
# print 1.0 * tf_trie[word] / isf_trie[word]
#
# word = u"ロゼ"
# print 1.0 * tf_trie[word] / isf_trie[word]
#
# word = u"ロゼワイン"
# print 1.0 * tf_trie[word] / isf_trie[word]
