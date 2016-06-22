# coding: utf-8

# edit distance of word level
# 1. Look for the correct word

# S: # of substitutions
# D: deletions
#
# | 0 |   1    |   2   | 3
# | 1 |        | apple | juice
# | 2 | apple  |       | Delet
# just calcualte from the left upper corner
import codecs
import os


def edit_distance(entry_one, entry_two):
    """
    The outer most arrays are "virtual" elements
    Assume entry_one as gold tokens
    Note that WER can be larger than 1.0
    :param entry_one:
    :param entry_two:
    :return:
    """
    assert len(entry_one) > 0 and len(entry_two) > 0
    entry_one.insert(0, "") # dummy
    entry_two.insert(0, "") # dummy
    two_dimentional_array = [[0 for i in range(len(entry_one))] for j in range(len(entry_two)) ]

    for j in range(len(entry_two)):
        two_dimentional_array[j][0] = j

    for i in range(len(entry_one)):
        two_dimentional_array[0][i] = i

    correct = 0
    for j in range(1, len(entry_two)):
        for i in range(1, len(entry_one)):
            up_left = two_dimentional_array[j - 1][i - 1] + 1
            up = two_dimentional_array[j][i - 1] + 1
            left = two_dimentional_array[j - 1][i] + 1

            if entry_one[i] == entry_two[j]:
                correct += 1
                # print entry_one[i], entry_two[j]
                up_left = two_dimentional_array[j - 1][i - 1]
            if entry_one[i - 1] == entry_two[j]:
                left = two_dimentional_array[j - 1][i]
            if entry_one[i] == entry_two[j - 1]:
                up = two_dimentional_array[j][i - 1]

            two_dimentional_array[j][i] = min(up, left, up_left)

    # removing dummies
    entry_one.pop(0)
    entry_two.pop(0)
    return two_dimentional_array[-1][-1], correct

def test_twitter_hashtag():
    f_gold = codecs.open("../data/test_data/leo_annotated/uniq_katakanas_ed.txt_overrided.txt", "r", "utf-8")
    f_predicted = codecs.open("../data/test_data/uniq_katakanas.txt_perceptron_tfisf_bigram_20151226", "r", "utf-8")
    calc_eval_metrics(f_gold, f_predicted)

def test_twitter_hashtag_oov():
    f_gold = codecs.open("data/test_data/uniq_katakanas.txt_oov_segmented.txt")
    f_predicted = codecs.open("data/test_data/uniq_katakanas.txt_oov.txt_perceptron_tfisf_bigram_20151226")
    calc_eval_metrics(f_gold, f_predicted)

def test_twitter_hashtag_oov_tfisf():
    f_gold = codecs.open("data/test_data/uniq_katakanas.txt_oov_segmented.txt")
    f_predicted = codecs.open("data/test_data/uniq_katakanas.txt_oov.txt_tfisf_result.txt")
    calc_eval_metrics(f_gold, f_predicted)

def test_twitter_hashtag_oov_kytea():
    f_gold = codecs.open("data/test_data/uniq_katakanas.txt_oov_segmented.txt")
    f_predicted = codecs.open("data/test_data/uniq_katakanas.txt_oov.txt_kytea_result.txt")
    calc_eval_metrics(f_gold, f_predicted)

def test_twitter_hashtag_latticelm():
    f_gold = codecs.open("../data/test_data/leo_annotated/uniq_katakanas_ed.txt_overrided.txt")
    f_predicted = codecs.open("out/samp.100")
    calc_eval_metrics(f_gold, f_predicted)

def calc_eval_metrics(f_gold, f_predicted):
    f_gold_lines = f_gold.readlines()
    f_predicted_lines = f_predicted.readlines()
    sum_correct_tokens = 0
    sum_gold_tokens = 0
    sum_predicted_tokens = 0
    sum_edit_distance = 0
    for i in range(len(f_gold_lines)):
        if not f_gold_lines[i].rstrip():
            continue  # skipping empty lines

        gold_tokens = f_gold_lines[i].rstrip().split()
        predicted_tokens = f_predicted_lines[i].rstrip().split(" ")

        edits, correct_tokens = edit_distance(gold_tokens, predicted_tokens)

        sum_edit_distance += edits
        sum_predicted_tokens += len(predicted_tokens)
        sum_gold_tokens += len(gold_tokens)

        correct_tokens_temp = compute_word_rawprec_rawrecall(gold_tokens, predicted_tokens)
        print "correct_tokens_temp: " + str(correct_tokens_temp)


        sum_correct_tokens += correct_tokens_temp
        print "gold data: " + " ".join(gold_tokens)
        print "prediction: " + " ".join(predicted_tokens)
        print str(edits) + " edits"
        print str(len(gold_tokens)) + " gold tokens"

    wer = 1.0 * sum_edit_distance / sum_gold_tokens
    print "WER = " + str(wer)
    precision = 1.0 * sum_correct_tokens / sum_predicted_tokens
    recall = 1.0 * sum_correct_tokens / sum_gold_tokens
    f1 = 2 * precision * recall / (precision + recall)
    print "precision = " + str(precision)
    print "recall = " + str(recall)
    print "f1 = " + str(f1)
    print "copy and paste the following lines to your .tex file"
    for_tex = (wer, precision, recall, f1)
    for_tex_tuples = map(lambda x: round(x, 3), for_tex)
    print "& %s & %s & %s & %s" % tuple(for_tex_tuples)


def compute_word_rawprec_rawrecall(gold_tokens, predicted_tokens):
    gold_labels = []
    predicted_labels = []
    for x in predicted_tokens:
        predicted_labels += ["0"] * (len(x) - 1) + ["1"]
    for y in gold_tokens:
        gold_labels += ["0"] * (len(y) - 1) + ["1"]

    # print predicted_labels
    j = 0
    temp_num_tokens = 0
    correct_tokens_temp = 0
    for k in range(len(gold_labels)):
        temp_num_tokens += int(gold_labels[k])
        if predicted_labels[k] == "1" and gold_labels[k] == "1":

            gold_label = "".join(gold_labels[j:k])
            predicted_label = "".join(predicted_labels[j:k])

            assert len(gold_label) == len(predicted_label)

            if len(gold_label) == 0:
                print
                "length of the gold label is one"
            if len(gold_label) == 0 and len(predicted_label) == 0:
                correct_tokens_temp += 1
            else:
                bitwise_result = int(gold_label, 2) ^ int(predicted_label, 2)
                # print "bitwise " + str(bitwise_result)
                if bitwise_result == 0:
                    correct_tokens_temp += temp_num_tokens
            j = k
            temp_num_tokens = 0
    return correct_tokens_temp


if __name__ == "__main__":
    assert edit_distance(["ab", "bc"], ["ab"])[0] == 1
    assert edit_distance(["abbc"], ["ab", "bc"])[0] == 2
    assert edit_distance(["ab", "bc"], ["a", "bbc"])[0] == 2

    # calc_eval_metrics(f_gold, f_predicted)
    test_twitter_hashtag()
    # test_twitter_hashtag_oov()
    # test_twitter_hashtag_oov_tfisf()
    # test_twitter_hashtag_latticelm()
    # test_twitter_hashtag_oov_kytea()
