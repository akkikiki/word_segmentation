# coding: utf-8

import codecs
import run_command

#def test_twitter_hashtag_oov():
#    in_file = "data/test_data/uniq_katakanas.txt_oov.txt"
#    run_kytea_on_testdata(in_file)


def run_kytea_on_testdata(in_file):
    run_command.preprocess_file(in_file)
    preprocessed_file_location = in_file + "_space_deleted.txt"
    run_kytea = 'kytea -model /Users/Fujinuma/Software/kytea-0.4.7/data/model.bin -notags < %s' % preprocessed_file_location
    stdout_data, _ = run_command.run_commnad(run_kytea)
    test_file_out = codecs.open(in_file + "_kytea_result.txt", "w")
    test_file_out.write(stdout_data)


in_file = "/data/test_data/uniq_katakanas.txt"

# run_kytea_on_testdata()
#test_twitter_hashtag_oov()
