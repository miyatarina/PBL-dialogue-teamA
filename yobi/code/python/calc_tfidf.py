import math
import collections
import sentencepiece as spm


model = spm.SentencePieceProcessor()
model.Load("PMIsentencepiece.model")


#北海道|宮城|東京|愛知|大阪|広島|愛媛|福岡
hokkaido = []
miyagi = []
tokyo = []
aichi = []
osaka = []
hiroshima = []
ehime = []
hukuoka = []

word_num = 0 #全単語数
word_count = collections.Counter()

with open("../mycollectPMIlocate2.txt", 'r') as f:
    for i, line in enumerate(f):
        line = line.strip()
        if "\t" in line:
            tag = line.rsplit("\t", 1)[0] #.replace("\t", " SEP ")
            txt = model.EncodeAsPieces(line.rsplit("\t", 1)[1])
            txt1 = txt[0].replace('▁', '')
            text = txt[1:]
            text.insert(0, txt1)

            word_num += len(text) #単語の数を加算 
            # print(len(text), text)
            word_count += collections.Counter(text) #カウンターを更新
            
            # 5単語以上のツイートを使用
            if len(text) >= 5:
                if tag == '<北海道>':
                    hokkaido.append(text)  # 分割したツイートを格納
                elif tag == '<宮城>':
                    miyagi.append(text)
                elif tag == '<東京>':
                    tokyo.append(text)
                elif tag == '<愛知>':
                    aichi.append(text)
                elif tag == '<大阪>':
                    osaka.append(text)
                elif tag == '<広島>':
                    hiroshima.append(text)
                elif tag == '<愛媛>':
                    ehime.append(text)
                elif tag == '<福岡>':
                    hukuoka.append(text)
                else:
                    continue

# len_num = float( len(hokkaido) + len(miyagi) + len(tokyo) + len(aichi) + len(osaka) + len(hiroshima) + len(ehime) + len(hukuoka) )


# ---- 各都道府県の文 ----
# hokkaido
# miyagi
# tokyo
# aichi
# osaka
# hiroshima
# ehime
# hukuoka

all_word = set()
# ---- TF の計算 ----
def calc_tf(prefecture):
    tf = {}
    for text in prefecture:
        word_count = collections.Counter()
        word_count += collections.Counter(text) # 文章内のある単語の出現回数
        length = len(text)
        for word in text:
            all_word.add(word)
            tf[word] = float(word_count[word]) / length
    return tf

# tf_hokkaido = {}
# for text in hokkaido:
#     word_count = collections.Counter()
#     word_count += collections.Counter(text) # 文章内のある単語の出現回数
#     length = len(text)
#     for word in text:
#         tf_hokkaido[word] = float(word_count[word]) / length

tf_hokkaido = calc_tf(hokkaido)
tf_miyagi = calc_tf(miyagi)
tf_tokyo = calc_tf(tokyo)
tf_aichi = calc_tf(aichi)
tf_osaka = calc_tf(osaka)
tf_hiroshima = calc_tf(hiroshima)
tf_ehime = calc_tf(ehime)
tf_hukuoka = calc_tf(hukuoka)


# ---- IDF の計算 ----

# def calc_idf(prefecture):
#     doc_num = len(prefecture) # 文書数
#     all_word = set()
#     for text in prefecture:
#         for word in text:
#             all_word.add(word)

#     idf = {}
#     for word in all_word:
#         # cnt = 0
#         # for text in prefecture:
#         #     if word in text:
#         #         cnt += 1
#         # idf[word] = math.log2(float(cnt)/doc_num) + 1

#         idf[word] = math.log2(8.0/doc_num) + 1
#     return idf


# log( 都道府県数 / その単語が出てきた都道府県数 )
idf = {}
for word in all_word:
    cnt = 0
    for text in hokkaido:
        if word in text:
            cnt += 1
            break
    for text in miyagi:
        if word in text:
            cnt += 1
            break
    for text in tokyo:
        if word in text:
            cnt += 1
            break
    for text in aichi:
        if word in text:
            cnt += 1
            break
    for text in osaka:
        if word in text:
            cnt += 1
            break
    for text in hiroshima:
        if word in text:
            cnt += 1
            break
    for text in ehime:
        if word in text:
            cnt += 1
            break
    for text in hukuoka:
        if word in text:
            cnt += 1
            break
    idf[word] = math.log2(8.0/cnt) + 1




# doc_num = len(hokkaido) # 文書数
# all_word = set()
# for text in hokkaido:
#     for word in text:
#         all_word.add(word)

# idf_hokkaido = {}
# for word in all_word:
#     cnt = 0
#     for text in hokkaido:
#         if word in text:
#             cnt += 1
#     idf_hokkaido[word] = math.log2(float(cnt)/doc_num) + 1

# idf_hokkaido = calc_idf(hokkaido)
# idf_miyagi = calc_idf(miyagi)
# idf_tokyo = calc_idf(tokyo)
# idf_aichi = calc_idf(aichi)
# idf_osaka = calc_idf(osaka)
# idf_hiroshima = calc_idf(hiroshima)
# idf_ehime = calc_idf(ehime)
# idf_hukuoka = calc_idf(hukuoka)


# ---- TF-IDF の計算 ----
def calc_tfidf(tf_dic, idf_dic):
    tf_idf = {}
    for word, tf in tf_dic.items():
        tf_idf[word] = idf_dic[word] * tf_dic[word]
    return tf_idf

tfidf_hokkaido = calc_tfidf(tf_hokkaido, idf)
tfidf_miyagi = calc_tfidf(tf_miyagi, idf)
tfidf_tokyo = calc_tfidf(tf_tokyo, idf)
tfidf_aichi = calc_tfidf(tf_aichi, idf)
tfidf_osaka = calc_tfidf(tf_osaka, idf)
tfidf_hiroshima = calc_tfidf(tf_hiroshima, idf)
tfidf_ehime = calc_tfidf(tf_ehime, idf)
tfidf_hukuoka = calc_tfidf(tf_hukuoka, idf)

with open("../TFIDF_kekka2.txt", 'w') as f:
    text = "hokkaido\n" + str(sorted(tfidf_hokkaido.items(), reverse=True, key=lambda x : x[1])) + "\nmiyagi\n" + str(sorted(tfidf_miyagi.items(), reverse=True, key=lambda x : x[1])) + "\ntokyo\n" + str(sorted(tfidf_tokyo.items(), reverse=True, key=lambda x : x[1])) + "\naichi\n" + str(sorted(tfidf_aichi.items(), reverse=True, key=lambda x : x[1])) + "\nosaka\n" + str(sorted(tfidf_osaka.items(), reverse=True, key=lambda x : x[1])) + "\nhiroshima\n" + str(sorted(tfidf_hiroshima.items(), reverse=True, key=lambda x : x[1])) + "\nehime\n" + str(sorted(tfidf_ehime.items(), reverse=True, key=lambda x : x[1])) + "\nhukuoka\n" + str(sorted(tfidf_hukuoka.items(), reverse=True, key=lambda x : x[1]))
    f.write(text)