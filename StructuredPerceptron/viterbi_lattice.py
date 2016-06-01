# coding: utf-8
import codecs
from collections import defaultdict
import math

from viterbi_node import Node

class BigramViterbiLattice(object):
    """
    This lattice will compute the best previous node.
    """

    def __init__(self, target_word, feature_weight_dicts, tf_trie, isf_trie, flags, blacklist_starting_char):
        self.unigram_bigram_weights = feature_weight_dicts[0] # unigram_bigram_weights, Featrue ID 2 in Kaji et al (2011)
        self.char_len_weights = feature_weight_dicts[1]
        # self.tfisf_weight = feature_weight_dicts[2]["tfisf_weight"]
        self.tf_trie = tf_trie
        self.isf_trie = isf_trie
        self.lattice_ending_at_j = [[] for j in range(len(target_word) + 2)] # x: word ending at indice x, y: list of words
        BOS_node = Node(u"BOS")
        EOS_node = Node(u"E")
        self.lattice_ending_at_j[0].append(BOS_node)
        self.lattice_ending_at_j[len(target_word) + 1].append(EOS_node)

        self.raw_unigram_flag = flags["raw_unigram_flag"]
        self.unigram_tfisf_flag = flags["tfisf"]
        self.bigram_flag = flags["bigram_flag"]
        self.char_len_flag = flags["char_len_flag"]
        self.debug_flag = flags["debug_flag"]
        self.non_initial_weight = flags["tfisf_not_initial_weights"]
        self.blacklist_starting_char = blacklist_starting_char

    def construct_lattice(self, target_word):
        """ what is needed
            1. the best word ending at indice i
            e.g. abc -> "a b c", "ab c", "a bc", "abc"
            * so for the indice 0, it is always the first character, in this case "a"
            * for 1, it is either "b" or "ab"
            * for 2, it is eiter "c", "bc" or "abc"
        """

        for i in range(len(target_word)):
            for j in range(i+1, len(target_word) + 1):
                substring = target_word[i:j]

                # Skipping a substring that starts with "ー"
                if len(target_word) != 1 and substring[0] in self.blacklist_starting_char:
                    continue

                substring_node = Node(substring)

                self.lattice_ending_at_j[j].append(substring_node) # building the Viterbi Lattice here
                # Then, refer to all possible previous substrings that ends at j - len(substring)
                self.choose_best_prev_substring(j)

        self.choose_best_prev_substring(j + 1)

        # Backword decoding
        return self.decode(target_word)


    def decode(self, target_word):
        decoded_segment = []
        j = len(target_word) + 1

        if target_word[0] in self.blacklist_starting_char:
            # just not segment it
            decoded_segment.append(target_word)
            return decoded_segment

        current_node = self.lattice_ending_at_j[j][0] # EOS_node
        current_node = current_node.best_prev_node

        while current_node.substring != u"BOS":
            decoded_segment.insert(0, current_node.substring)
            current_node = current_node.best_prev_node
        return decoded_segment

    def choose_best_prev_substring(self, j):
        """ Refer to list of possible previous substrings
        :param j:
        :param current_substring:
        :return:
        """
        # the last added node
        current_substring_node = self.lattice_ending_at_j[j][len(self.lattice_ending_at_j[j]) - 1]
        current_substring = current_substring_node.substring

        prev_substring_nodes = self.lattice_ending_at_j[j - len(current_substring)]
        best_score = None
        if current_substring in self.tf_trie and current_substring in self.isf_trie:
            ts_isf_val = self.tf_trie[current_substring][0][0] * 1.0 / self.isf_trie[current_substring][0][0]
        else:
            ts_isf_val = 0

        for prev_substring_node in prev_substring_nodes:
            bigram = prev_substring_node.substring + u"," + current_substring

            current_score = prev_substring_node.score

            if self.bigram_flag:
                current_score += 1.0 * self.unigram_bigram_weights.get(bigram, 0)

            if self.char_len_flag:
                current_score += self.char_len_weights.get(len(current_substring), 0)

            if self.unigram_tfisf_flag:
                if self.non_initial_weight:
                    current_score += self.unigram_bigram_weights.get(current_substring, 1) * math.log(ts_isf_val + 1)
                else:
                    # current_score += self.unigram_bigram_weights.get(current_substring, 1) + math.log(ts_isf_val + 1) # update the weights
                    current_score += self.unigram_bigram_weights.get(current_substring, 0) + math.log(ts_isf_val + 1) # update the weights
                # always include tfisf even it did not appear in the training data
                if self.debug_flag:
                    print math.log(ts_isf_val + 1)
                    print current_substring, self.unigram_bigram_weights.get(current_substring, 1) + math.log(ts_isf_val + 1)
                    # print current_substring, self.unigram_bigram_weights.get(current_substring, 1) * math.log(ts_isf_val + 1)
                    # print current_substring, self.unigram_bigram_weights.get(current_substring, 1) * ts_isf_val

            if self.raw_unigram_flag and not self.unigram_tfisf_flag:
                current_score += 1.0 * self.unigram_bigram_weights.get(current_substring, 0)


            # print bigram, current_score, best_score

            if (best_score is None) or (current_score >= best_score):
                best_score = current_score
                current_substring_node.best_prev_node = prev_substring_node
                current_substring_node.score = current_score
        # So for each substring (node), we set the best previous node

if __name__ == "__main__":
    in_file = "/Users/Fujinuma/PycharmProjects/katakana-segmentation/compound_segmentation/data/fujinuma_annotated/catted_hashtag_ranking_uniigramcount_katakana_only.head500.replaced.txt"
    test_file = codecs.open(in_file, "r", "utf-8")
    # test_file_out = codecs.open(in_file + "_tfisf_result.txt", "w", "utf-8")
    test_file_out = codecs.open(in_file + "_tfisf_sum_isf_over_sum_tf_result.txt", "w", "utf-8")
    for katakana in test_file:
        tfisf_viterbi_lattice = BigramViterbiLattice(katakana[:-1])
        decoded_segments = tfisf_viterbi_lattice.construct_lattice(katakana[:-1])
        print katakana[:-1] + " -> " + " ".join(decoded_segments)
        test_file_out.write(" ".join(decoded_segments).rstrip() + "\n")
