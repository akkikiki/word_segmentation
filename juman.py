# coding: utf-8

from pyknp import Juman
import sys
import codecs
 
juman = Juman()

input_file = "../data/sample.txt"
f = codecs.open(input_file, 'r', 'utf-8')
f_out = codecs.open(input_file + '_juman_result.txt','w', 'utf-8')
for line in f:
    result = juman.analysis(line[:-1].replace(" ", ""))
    #print ' '.join(mrph.midasi for mrph in result)
    f_out.write(' '.join(mrph.midasi for mrph in result) + '\n')
