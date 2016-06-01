# coding: utf-8
import codecs
import math
import pickle

data = open('data/tfisf/tf_trie_20151226.txt', 'rb')
tf_trie = pickle.load(data)
freq_dic = {}

def heuristics_based_method(geo_mean_freq, avg_substr_len):
    C = 1.0 * 2500
    N = 1.0 * 4
    alpha = 0.7

    score = 1.0 * geo_mean_freq / (C / (math.pow(N, avg_substr_len) + alpha))
    return score

def calc_score_katakana(substring_seq):
    length_sum = 0
    freq_product = 1

    for elem in substring_seq:
        length_sum += len(elem)
        if elem in tf_trie:
            freq_product *= tf_trie[elem][0][0]
        else:
            freq_product *= 0

    freq_geo_mean = math.pow(freq_product, 1.0/len(substring_seq))
    length_avg = 1.0 * length_sum / len(substring_seq)
    score = heuristics_based_method(freq_geo_mean, length_avg)

    if len(substring_seq) == 1 and substring_seq[0] in tf_trie:
        # score = freq_geo_mean
        score = tf_trie[substring_seq[0]][0][0]

    return score


def segment_katakana(compound_word_candidate):
    substring_sequences = []

    for i in range(1 << len(compound_word_candidate) - 1):
        substring_sequence = []
        substring = "" # assuming len > 0
        for j in range(len(compound_word_candidate)):
            segment_or_not = i & 1;
            substring += compound_word_candidate[j]
            if segment_or_not == 1:
                substring_sequence.append(substring)
                substring = ""
            i = i >> 1
        substring_sequence.append(substring)
        substring_sequences.append(substring_sequence)
    return substring_sequences

def segment_katakana_select_max_seq(compound_word_candidate):
    max_substring_sequence = []
    max_score = 0

    # skipping for extremely long compund word
    if len(compound_word_candidate) > 20:
        max_substring_sequence.append(compound_word_candidate)
        return max_substring_sequence
#     max_substr_seq = substr_seqs[0]

    for i in range(1 << len(compound_word_candidate) - 1):
        substring_sequence = []
        substring = "" # assuming len > 0
        for j in range(len(compound_word_candidate)):
            segment_or_not = i & 1;
            substring += compound_word_candidate[j]
            if segment_or_not == 1:
                substring_sequence.append(substring)
                substring = ""
            i = i >> 1
        substring_sequence.append(substring)
        if max_score < calc_score_katakana(substring_sequence):
            max_score = calc_score_katakana(substring_sequence)
            max_substring_sequence = substring_sequence
        # substring_sequences.append(substring_sequence)
    return max_substring_sequence

# def select_max_score_seq(substr_seqs):
#     max_score = 0
#     max_substr_seq = substr_seqs[0]
#     for elem in substr_seqs:
#         # print " ".join(elem) + ": " + str(calc_score_katakana(elem))
#         if max_score < calc_score_katakana(elem):
#             max_score = calc_score_katakana(elem)
#             max_substr_seq = elem
#
#     no_segments = "".join(substr_seqs[0])
#     freq_no_segments = 0
#     if no_segments in tf_trie:
#         freq_no_segments = tf_trie[no_segments][0][0]
#
#     if freq_no_segments > max_score:
#         # discard if the score is less than the freq of compound word candidate
#         return substr_seqs[0]
#
#     return max_substr_seq


if __name__ == "__main__":
    compound_word_candidates = [u'プログラマーコンテスト', u'プログラミングコンテスト', u'ロゼワイン', u'ヱビスビール', u'クラフトビール', u'ワインバーグ',
                                u'スマホケースカバー', u'レインボー', u'コネティカット',
                                u'スマホケースカバー', u'フレーバードワイン', u'スパークリングワイン', u'スパイスライス',
                                u'メタリックタトゥーシール', u'コリアンダースパイシーサラダ', u'デイジーダック',
                                u'ドイトンコーヒー', u'ワンタッチタープテント', u'タピオカジュース', u'ロックフェス',
                                u'ロープライス', u'ガソリンスタンド', u'コピペブログ', u'マイクロソフトオフィス',
                                u'ブラキッシュレッド', u'ウォーターサーバ', u'ハッシュドビーフソース', u'ワンダースワン',
                                u'トンコツラーメン', u'トラッキングスパム', u'ジャンクフード', u'アンチョビパスタ',
                                u'グーグルマップ', u'ソーシャルネットワーキングサービス', u'ライブドアニュース',
                                u'サントリービール', u'カスタマーサービス', u'グリーンスムージーダイエット', u'マジリスペクト',
                                u'ユーザカンファレンス', u'ランチタイム', u'サイエンスカフェ', u'スマホスタンド', u'ネットカフェ',
                                u'オレンジジュース', u'リケジョカフェ', u'リケジョサイエンスカフェ', u'チーズバーガー', u'ハンバーガー',
                                u'プライベートリポジトリ', u'フェイスブック', u'コミットメッセージ', u'マシンラーニング', u'アニメオタク',
                                u'オーブントースター', u'マイナスイメージ', u'ワンルームマンション', u'アルバイトスタッフ', u'リサイクルショップ',
                                u'トークンクレデンシャル', u'シグニチャベースストリング', u'リモートビルド', u'オルタナティブブログ',
                                u'フレームワーク', u'レオナルドダヴィンチ', u'アイポッドナノ', u'アイポッドタッチ', u'マイケルジャクソン',
                                u'バラクオバマ', u'スターウォーズ', u'ビンテージコーヒー', u'ランニングホームラン', u'スパイスガールズ',
                                u'ランニングシューズ', u'ランニングスタイル', u'ランニングシャツ', u'アミューズメントプランニング',
                                u'フレームガンダム', u'ガンダム', u'ワークショップ', u'ジュラシックパーク', u'アボカドベジタブルチキン',
                                u'ウォッシャブルマルチトリマー',
                                u'タイムマネジメント', u'ロジカルフローグラフ', u'ソリューションプロジェクト']

    # for katakana in compound_word_candidates:
    #     a = segment_katakana(katakana)
    #     max_substr_seq = select_max_score_seq(a)
    #     print katakana + " -> " + " ".join(max_substr_seq)

    # test_file = codecs.open("katakana_samples.txt", "r", "utf-8")
    test_filename = "data/test_data/uniq_katakanas.txt"
    test_file = codecs.open(test_filename, "r", "utf-8")
    # test_file_out = codecs.open("katakana_segment_sample_results_nakazawa.txt", "w", "utf-8")
    test_file_out = codecs.open(test_filename + "_nakazawa_results.txt", "w", "utf-8")
    for katakana in test_file:
        # a = segment_katakana(katakana[:-1])
        max_substr_seq = segment_katakana_select_max_seq(katakana[:-1])
        # max_substr_seq = select_max_score_seq(a)
        print katakana[:-1] + " -> " + " ".join(max_substr_seq)
        test_file_out.write(" ".join(max_substr_seq).rstrip() + "\n")
