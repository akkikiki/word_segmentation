# coding: utf-8
import codecs
import run_command

run_mecab_ipa = 'echo %s | mecab' % u"今日は天気がいい"
stdout_data, _ = run_command.run_commnad(run_mecab_ipa)

# parse_segmentation(stdout_data)

in_file = "sample.txt"
test_file_out = codecs.open(in_file + "_mecab_ipadic_result.txt", "w")

run_command.preprocess_file(in_file)

temp_file = in_file + "_space_deleted.txt"

# run_mecab_ipa = 'mecab %s' % in_file
run_mecab_ipa = 'mecab %s' % temp_file
stdout_data, _ = run_command.run_commnad(run_mecab_ipa)
run_command.parse_segmentation(stdout_data, test_file_out)

run_mecab_unidic = 'mecab --dicdir=/usr/local/lib/mecab/dic/unidic %s' % temp_file # run with unidic
unidic_result_file = codecs.open(in_file + "_mecab_unidic_result.txt", "w")
stdout_data, _ = run_command.run_commnad(run_mecab_unidic)
run_command.parse_segmentation(stdout_data, unidic_result_file)

