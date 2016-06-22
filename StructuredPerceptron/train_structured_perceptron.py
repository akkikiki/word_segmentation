# coding: utf-8

import codecs
import re
from collections import defaultdict
from hat_trie import Trie
import pickle
from viterbi_lattice import BigramViterbiLattice

UNIGRAM_ISF = "tfisf"
model = "tfisf_bigram_20151226"
model_name = "katakana_feature_weights_%s.txt" % model
read_existing_model = False

class StructuredPerceptron(object):
    def __init__(self, model_name):
        #self.training_filename = training_dir + "katakanaRuleBasedTrainingExamplesWithSpace_no_occurence.txt"
        self.training_filename = "../data/sample.txt"
        weight_unigram_bigram_dic = Trie()  # Featrue ID 1 and 2 in Kaji et al (2011)
        weight_char_len_dic = defaultdict(int)  # Feature ID 3 in Kaji et al (2011)
        self.feature_weight_dicts = [weight_unigram_bigram_dic, weight_char_len_dic]

        # data = open('../data/tfisf/tf_trie.txt', 'rb')
        # data = open('../data/tfisf/tf_trie_20151226.txt', 'rb')
        # self.tf_trie = pickle.load(data)
        # isf_data = open('../data/tfisf/isf_trie.txt', 'rb')
        # isf_data = open('../data/tfisf/isf_trie_20151226.txt', 'rb')
        # self.isf_trie = pickle.load(isf_data)

        flags = {}
        flags["averaged_perceptron"]  = False
        flags[UNIGRAM_ISF]            = True
        flags["raw_unigram_flag"]     = False
        flags["bigram_flag"]          = True
        flags["char_len_flag"]        = False
        flags["debug_flag"]           = False
        flags["exclude_zero_weights"] = True
        flags["tfisf_not_initial_weights"] = False
        self.flags = flags
        self.learning_rate = 1
        self.blacklist_starting_char = [u"ー", u'ァ', u'ィ', u'ゥ', u'ェ',u'ォ', u'ヵ', u'ヶ', u'ッ', u'ャ', u'ュ', u'ョ', u'ヮ']

    def train_structured_perceptron(self):
        f_weights = codecs.open(model_name, "w", "utf-8")
        N = 10
        c = 1  # Training iteration
        W_a = defaultdict(int)  # used for calculating averaged perceptron

        for i in range(N):
            print "Training Iteration: " + str(i + 1)

            training_samples = codecs.open(self.training_filename, "r", "utf-8")
            for train_data in training_samples:
                # print "The num of entries in bigram dic is " + str(len(weight_unigram_bigram_dic))

                # skip the if it starts from "ー", etc.
                if train_data[0] in self.blacklist_starting_char:
                    print "Skipping: " + train_data[:-1]
                    continue

                words = re.sub(u' +', u' ', train_data[:-1])
                X_words = words.split(u' ')
                input_string = ''.join(X_words)
                bigram_viterbi_lattice = BigramViterbiLattice(input_string, self.feature_weight_dicts, self.tf_trie,
                                                              self.isf_trie, self.flags, self.blacklist_starting_char)
                Y_hat = bigram_viterbi_lattice.construct_lattice(input_string)

                resulting_word = ' '.join(Y_hat)

                # only when the segmentation results differ,
                # if resulting_word != train_data:
                if resulting_word != words:
                    self.increment_feature_value(W_a, X_words, c, self.learning_rate, self.feature_weight_dicts)
                    self.increment_feature_value(W_a, Y_hat, c, -1 * self.learning_rate, self.feature_weight_dicts)

                    c += 1

        weight_unigram_bigram_dic = self.feature_weight_dicts[0]
        weight_char_len_dic = self.feature_weight_dicts[1]
        print "Now saving the model..."
        for k in weight_unigram_bigram_dic.keys():
            v = weight_unigram_bigram_dic[k]

            if v == 0 and self.flags["exclude_zero_weights"]:
                continue

            if self.flags["averaged_perceptron"]:
                # print k, str(v - (1.0 * W_a[k] / c)) # feature values with averaged perceptron
                f_weights.write(k + "\t" + str(v - (1.0 * W_a[k] / c)) + "\n") # feature values with averaged perceptron
            else:
                f_weights.write(k + "\t" + str(v) + "\n")  # outputting feature weights


        for k, v in weight_char_len_dic.items():
            f_weights.write(str(k) + "\t" + str(v) + "\n")  # outputting feature weights
            # print k, str(v)

    def increment_feature_value(self, W_a, X_words, c, increment_value, feature_weight_dicts):
        weight_unigram_bigram_dic = feature_weight_dicts[0]
        weight_char_len_dic = feature_weight_dicts[1]

        for i, token in enumerate(X_words):

            if self.flags["char_len_flag"]:
                if len(token) >= 5:
                    weight_char_len_dic[5] = weight_char_len_dic.get(5, 0) + increment_value
                else:
                    weight_char_len_dic[len(token)] = weight_char_len_dic.get(len(token), 0) + increment_value

            if self.flags["bigram_flag"]:
                key = ""
                if i == 0:
                    key = u"BOS," + token
                else:
                    key = X_words[i - 1] + u"," + token

                weight_unigram_bigram_dic[key] = weight_unigram_bigram_dic.get(key, 0) + increment_value

                if self.flags["averaged_perceptron"]:
                    W_a[key] = weight_unigram_bigram_dic.get(key, 0) + c * increment_value

            if self.flags[UNIGRAM_ISF] or self.flags["raw_unigram_flag"]:
                weight_unigram_bigram_dic[token] = weight_unigram_bigram_dic.get(token, 0) + increment_value

                if self.flags["averaged_perceptron"]:
                    W_a[token] = weight_unigram_bigram_dic.get(token, 0) + c * increment_value


    def train_partially_labled_structured_perceptron(self):
        # Incorporates the assumption that NOT ALL OF THE SEGMENTS ARE LABELLED
        f_weights = codecs.open(model_name + "_partially_labeled_perceptron.txt", "w", "utf-8")
        # N = 10
        N = 1 # starting from small iterations since 1 iteration takes around 100mins
        c = 1  # Training iteration
        W_a = defaultdict(int)  # used for calculating averaged perceptron
        count_tracker = 1

        for i in range(N):
            print "Training Iteration: " + str(i + 1)

            training_samples = codecs.open(self.training_filename, "r", "utf-8")
            for train_data in training_samples:

                # print "The num of entries in bigram dic is " + str(len(weight_unigram_bigram_dic))
                words = re.sub(u' +', u' ', train_data[:-1])
                X_words = words.split(u' ')

                # skip the if it starts from "ー"
                skip_flag = False
                for word in X_words:
                    if word[0] in self.blacklist_starting_char:
                        print "Skipping: " + train_data[:-1]
                        skip_flag = True
                if skip_flag:
                    continue


                input_string = ''.join(X_words)
                bigram_viterbi_lattice = BigramViterbiLattice(input_string, self.feature_weight_dicts, self.tf_trie,
                                                              self.isf_trie, self.flags, self.blacklist_starting_char)
                Y_hat = bigram_viterbi_lattice.construct_lattice(input_string)

                Y_hat_constarined = []
                for partially_labeled_word in X_words:
                    bigram_viterbi_lattice = BigramViterbiLattice(partially_labeled_word, self.feature_weight_dicts, self.tf_trie,
                                                              self.isf_trie, self.flags, self.blacklist_starting_char)
                    Y_hat_constarined.extend(bigram_viterbi_lattice.construct_lattice(partially_labeled_word))

                constrained_resulting_word = ' '.join(Y_hat_constarined) # debug purpose

                resulting_word = ' '.join(Y_hat)

                # only when the segmentation results differ,
                if self.violates(resulting_word, train_data):
                    # print resulting_word, train_data
                    # self.increment_feature_value(W_a, X_words, c, 1, self.feature_weight_dicts)
                    # self.increment_feature_value(W_a, X_words, c, self.learning_rate, self.feature_weight_dicts)
                    self.increment_feature_value(W_a, Y_hat_constarined, c, self.learning_rate, self.feature_weight_dicts)
                    self.increment_feature_value(W_a, Y_hat, c, -1 * self.learning_rate, self.feature_weight_dicts)
                    # self.increment_feature_value(W_a, Y_hat, c, -1, self.feature_weight_dicts)

                    # print "updated using %s" % words
                # else:
                #     print "skipping %s" % words

                c += 1

                if c > count_tracker * 10000:
                    print "finished %s examples" % str(c)
                    count_tracker += 1


        weight_unigram_bigram_dic = self.feature_weight_dicts[0]
        # print 'printing feature weights in bigram dic-----'
        for k in weight_unigram_bigram_dic.keys():
            v = weight_unigram_bigram_dic[k]
            f_weights.write(k + "\t" + str(v) + "\n")  # outputting feature weights

    def violates(self, resulting_word, partially_labeled_word):
        indice_resulting_word = 0
        indice_partially_labeled = 0
        while indice_partially_labeled < len(partially_labeled_word) and indice_resulting_word < len(resulting_word):
            if resulting_word[indice_resulting_word] == partially_labeled_word[indice_partially_labeled]:
                indice_resulting_word += 1
                indice_partially_labeled += 1
                continue

            if resulting_word[indice_resulting_word] == " " and partially_labeled_word[indice_partially_labeled] != " ":
                indice_resulting_word += 1
                continue

            if resulting_word[indice_resulting_word] != " " and partially_labeled_word[indice_partially_labeled] == " ":
                return True

        return False

    def test_structured_perceptron(self, input_string):
        """
        Reading feature weights from the saved file
        :param input_string:
        :return:
        """

        bigram_viterbi_lattice = BigramViterbiLattice(input_string, self.feature_weight_dicts, self.tf_trie,
                                                      self.isf_trie, self.flags, self.blacklist_starting_char)
        Y_hat = bigram_viterbi_lattice.construct_lattice(input_string)
        resulting_word = ' '.join(Y_hat)

        return resulting_word

    def test_infile(self, in_file):
        f = codecs.open(in_file, "r", "utf-8")

        # out_file = in_file + "_perceptron_tfisf_bigram_eta0.1"
        # out_file = in_file + "_perceptron_tfisf_20151226"
        # out_file = in_file + "_perceptron_tfisf_20151226_log_isf"
        out_file = in_file + "_perceptron_" + model
        # out_file = in_file + "_perceptron_tfisf_bigram_20151226"
        # out_file = in_file + "_perceptron_tfisf_bigram_averaged_20151226"
        # out_file = in_file + "_perceptron_raw_unigram_20151226"
        # out_file = in_file + "_perceptron_raw_unigram_bigram_20151226"
        f_out = codecs.open(out_file, "w", "utf-8")

        for line in f:
            test_string = line[:-1]
            result = self.test_structured_perceptron(test_string)
            f_out.write(result + "\n")
            print test_string + " -> " + result

    def read_model(self):
        weight_unigram_bigram_dic = Trie()      # Featrue ID 1 and 2 in Kaji et al (2011)
        weight_char_len_dic = defaultdict(int)  # Feature ID 3 in Kaji et al (2011)
        f_weights = codecs.open(model_name, "r", "utf-8")  # opening the trained model file
        for line in f_weights:
            feature, weight = line[:-1].split("\t")
            if feature in ["1", "2", "3", "4", "5"]:
                weight_char_len_dic[feature] = int(weight)

            # weight_unigram_bigram_dic[feature] = int(weight)  # or float type?
            weight_unigram_bigram_dic[feature] = float(weight)
        self.feature_weight_dicts = [weight_unigram_bigram_dic, weight_char_len_dic]  # , weight_tfisf_dic]

    def test_katakana_hashtags(self):
        self.read_model() # First, read and parse the model from a file
        in_file = "../data/test_data/uniq_katakanas.txt"
        self.test_infile(in_file)

    def test_katakana_hashtags_oov(self):
        # run count_oov_in_hashtags.py beforehand to produce "data/test_data/uniq_katakanas.txt_oov.txt"
        self.read_model()
        in_file = "../data/test_data/uniq_katakanas.txt_oov.txt"
        self.test_infile(in_file)

    def test_katakana_samples(self):
        self.read_model()
        katakana_words = [u"アンコールトム", u"マヌカハニー", u"プログラマーコンテスト", u"ミニスカポリス", u"ヴァイスシュヴァルツ",
                          u"セカイノオワリ", u"ブロンズプライズ", u"アラームクロック"]

        for word in katakana_words:
            result = self.test_structured_perceptron(word)
            print word + " -> " + result

# TODO: Implement paraphrase feature weight.

if __name__ == "__main__":
    perceptron = StructuredPerceptron(model_name)
    perceptron.train_structured_perceptron() # train a model
    # perceptron.train_partially_labled_structured_perceptron() # train a model
    # perceptron.test_infile(in_file)  # test a model
    perceptron.test_katakana_hashtags()  # test a model on katakana hashtags
    # perceptron.test_katakana_samples()
    # perceptron.test_katakana_hashtags_oov()

"""
Y_hat: The most probably segmentation
- Given the observed katakana seq. X
- currently, the feature (and compute_score) is only a single token in X
"""
