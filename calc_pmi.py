import MeCab
import argparse
import os
import math
import collections
import sentencepiece as spm

# parser = argparse.ArgumentParser()
# parser.add_argument('-lf',  type=str, help='load file help')

# opt = parser.parse_args()

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

location_num = float( len(hokkaido) + len(miyagi) + len(tokyo) + len(aichi) + len(osaka) + len(hiroshima) + len(ehime) + len(hukuoka) )
# ---- P(y)の計算 ----
py_hokkaido = len(hokkaido) / location_num
py_miyagi = len(miyagi) / location_num
py_tokyo = len(tokyo) / location_num
py_aichi = len(aichi) / location_num
py_osaka = len(osaka) / location_num
py_hiroshima = len(hiroshima) / location_num
py_ehime = len(ehime) / location_num
py_hukuoka = len(hukuoka) / location_num

# ---- P(x)の計算 ---- 辞書型 (word: 確率)
px = {}
for word, count in word_count.most_common():
    px[word]=float(count)/word_num 

all_word = word_count.keys()
# ---- P(x,y)の計算 ---- 

pxy_hokkaido = {}
for word in all_word: #ある単語が
    cooc = 0 #共起回数
    for text in hokkaido:
        if word in text: #北海道の中に含まれていれば
            cooc += 1
    pxy_hokkaido[word] = float(cooc)/location_num

pxy_miyagi = {}
for word in all_word:
    cooc = 0
    for text in miyagi:
        if word in text: 
            cooc += 1
    pxy_miyagi[word] = float(cooc)/location_num

pxy_tokyo = {}
for word in all_word:
    cooc = 0
    for text in tokyo:
        if word in text: 
            cooc += 1
    pxy_tokyo[word] = float(cooc)/location_num

pxy_aichi = {}
for word in all_word:
    cooc = 0
    for text in aichi:
        if word in text: 
            cooc += 1
    pxy_aichi[word] = float(cooc)/location_num

pxy_osaka = {}
for word in all_word:
    cooc = 0
    for text in osaka:
        if word in text: 
            cooc += 1
    pxy_osaka[word] = float(cooc)/location_num

pxy_hiroshima = {}
for word in all_word:
    cooc = 0
    for text in hiroshima:
        if word in text: 
            cooc += 1
    pxy_hiroshima[word] = float(cooc)/location_num

pxy_ehime = {}
for word in all_word:
    cooc = 0
    for text in ehime:
        if word in text: 
            cooc += 1
    pxy_ehime[word] = float(cooc)/location_num

pxy_hukuoka = {}
for word in all_word:
    cooc = 0
    for text in hukuoka:
        if word in text: 
            cooc += 1
    pxy_hukuoka[word] = float(cooc)/location_num



# P(x) : 単語xの出現確率  = 単語xの出現回数 / 全単語数
# P(y) : 地域yの出現確率  = 地域yの出現回数 / 全ツイート件数
# P(x,y) : 地域yのツイートに単語xが含まれる確率(共起数)  = 単語xが含まれる地域yのツイート / 全ツイート件数
# PMI(x,y) = log_2 P(x,y)/P(x)×P(y)
#参考文献: https://camberbridge.github.io/2016/07/08/%E8%87%AA%E5%B7%B1%E7%9B%B8%E4%BA%92%E6%83%85%E5%A0%B1%E9%87%8F-Pointwise-Mutual-Information-PMI-%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6/


# -----PMIの計算------
# pmi = math.log2( pxy / (px * py) )

# key:単語 value:PMI 
pmi_hokkaido = {}
for key, _ in pxy_hokkaido.items():
    if (pxy_hokkaido[key] / (px[key] * py_hokkaido)) > 0:
        pmi_hokkaido[key] = math.log2(pxy_hokkaido[key] / (px[key] * py_hokkaido))
print("hokkaido\n", sorted(pmi_hokkaido.items(), reverse=True, key=lambda x : x[1]))

pmi_miyagi = {}
for key, _ in pxy_miyagi.items():
    if (pxy_miyagi[key] / (px[key] * py_miyagi)) > 0:
        pmi_miyagi[key] = math.log2(pxy_miyagi[key] / (px[key] * py_miyagi))
print("miyagi\n", sorted(pmi_miyagi.items(), reverse=True, key=lambda x : x[1]))

pmi_tokyo = {}
for key, _ in pxy_tokyo.items():
    if (pxy_tokyo[key] / (px[key] * py_tokyo)) > 0:
        pmi_tokyo[key] = pxy_tokyo[key] * math.log2(pxy_tokyo[key] / (px[key] * py_tokyo))
print("tokyo\n", sorted(pmi_tokyo.items(), reverse=True, key=lambda x : x[1]))

pmi_aichi = {}
for key, _ in pxy_aichi.items():
    if (pxy_aichi[key] / (px[key] * py_aichi)) > 0:
        pmi_aichi[key] = math.log2(pxy_aichi[key] / (px[key] * py_aichi))
print("aichi\n", sorted(pmi_aichi.items(), reverse=True, key=lambda x : x[1]))

pmi_osaka = {}
for key, _ in pxy_osaka.items():
    if (pxy_osaka[key] / (px[key] * py_osaka)) > 0:
        pmi_osaka[key] = pxy_osaka[key] * math.log2(pxy_osaka[key] / (px[key] * py_osaka))
print("Osaka\n", sorted(pmi_osaka.items(), reverse=True, key=lambda x : x[1]))


pmi_hiroshima = {}
print(pxy_hiroshima)
for key, _ in pxy_hiroshima.items():
    print(pxy_hiroshima[key], px[key], py_hiroshima)
    if (pxy_hiroshima[key] / (px[key] * py_hiroshima)) > 0:
        pmi_hiroshima[key] = math.log2(pxy_hiroshima[key] / (px[key] * py_hiroshima))
print("hiroshima\n", sorted(pmi_hiroshima.items(), reverse=True, key=lambda x : x[1]))

pmi_ehime = {}
for key, _ in pxy_ehime.items():
    if (pxy_ehime[key] / (px[key] * py_ehime)) > 0:
        pmi_ehime[key] = math.log2(pxy_ehime[key] / (px[key] * py_ehime))
print("ehime\n", sorted(pmi_ehime.items(), reverse=True, key=lambda x : x[1]))

pmi_hukuoka = {}
for key, _ in pxy_hukuoka.items():
    if (pxy_hukuoka[key] / (px[key] * py_hukuoka)) > 0:
        pmi_hukuoka[key] = math.log2(pxy_hukuoka[key] / (px[key] * py_hukuoka))
print("hukuoka\n", sorted(pmi_hukuoka.items(), reverse=True, key=lambda x : x[1]))


with open("../PMI_kekka.txt", 'w') as f:
    text = "hokkaido\n" + str(sorted(pmi_hokkaido.items(), reverse=True, key=lambda x : x[1])) + "\nmiyagi\n" + str(sorted(pmi_miyagi.items(), reverse=True, key=lambda x : x[1])) + "\ntokyo\n" + str(sorted(pmi_tokyo.items(), reverse=True, key=lambda x : x[1])) + "\naichi\n" + str(sorted(pmi_aichi.items(), reverse=True, key=lambda x : x[1])) + "\nosaka\n" + str(sorted(pmi_osaka.items(), reverse=True, key=lambda x : x[1])) + "\nhiroshima\n" + str(sorted(pmi_hiroshima.items(), reverse=True, key=lambda x : x[1])) + "\nehime\n" + str(sorted(pmi_ehime.items(), reverse=True, key=lambda x : x[1])) + "\nhukuoka\n" + str(sorted(pmi_hukuoka.items(), reverse=True, key=lambda x : x[1]))
    f.write(text)

# print(len(tokyo))
# print(len(ehime))