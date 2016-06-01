# coding: utf-8
import marisa_trie
import pickle
import math

#tf_trie = marisa_trie.Trie()
#tf_trie.load('my_trie_copy.marisa')
#data = open('tf_trie.txt', 'rb')
data = open('tf_trie.txt', 'rb')
tf_trie = pickle.load(data)
isf_data = open('isf_trie.txt', 'rb')
#isf_data = open('isf_trie.pickle', 'rb')
isf_trie = pickle.load(isf_data)

words = [u"ワイン", u"ロゼ", u"ロゼワイン", u"ビール", u"ヱビスビール", u"ヱビス", u"ワ", u"リング"]

for word in words:
    print word + str(1.0 * tf_trie[word][0][0] * 1.0 / isf_trie[word][0][0])
    print tf_trie[word][0][0]
    print isf_trie[word][0][0]

def extract_segmented_substrings(word): 
    substrings = []
    for i in range(len(word)):
        for j in range(i+1, len(word) + 1):
            substrings.append(word[i:j])
    return substrings

compound_words = [u'プログラマーコンテスト', u'ロゼワイン', u'ヱビスビール', u'クラフトビール', u'ワインバーグ', u'スマホケース', u'フレーバードワイン', u'スパークリングワイン', u'スパイスライス', u'メタリックタトゥーシール', u'コリアンダースパイシーサラダ', u'デイジーダック', u'ドイトンコーヒー', u'ワンタッチタープテント', u'タピオカジュース', u'ロックフェス', u'ロープライス', u'ガソリンスタンド', u'コピペブログ', u'マイクロソフトオフィス', u'ブラキッシュレッド', u'ウォーターサーバ', u'ハッシュドビーフソース', u'ワンダースワン', u'トンコツラーメン', u'トラッキングスパム', u'ジャンクフード', u'アンチョビパスタ', u'グーグルマップ', u'ソーシャルネットワーキングサービス', u'ライブドアニュース', u'サントリービール', u'カスタマーサービス', u'グリーンスムージーダイエット', u'マジリスペクト', u'ユーザカンファレンス']

for word in compound_words:
    substrings = extract_segmented_substrings(word)
    print substrings
    for string in substrings:
        if string in tf_trie and string in isf_trie:
            print string + str(1.0 * tf_trie[string][0][0] * 1.0 / isf_trie[string][0][0])
