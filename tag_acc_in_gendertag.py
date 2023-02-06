import numpy as np
import sys
import sentencepiece as spm
from tqdm import tqdm
from collections import defaultdict

def make_dic():
    d = defaultdict(float)
    dic = {}
    flag = False
    if sys.argv[2] == "pmi":
        fin = open("PMI_lines.txt", "r")
    elif sys.argv[2] == "localpmi":
        fin = open("localPMI_lines.txt", "r")
    elif sys.argv[2] == "tfidf":
        fin = open("TFIDF_lines.txt", "r")
    else:
        print("usage: python %s {max, ave} {pmi, localpmi, tfidf} {acc, [filename]}" % sys.argv[0])
        sys.exit()
    for line in fin:
        if "\t" not in line:
            if " " in line:
                continue
            if flag:
                dic[kenmei] = d
                d = defaultdict(float)
            kenmei = line.strip()
            flag = True
        else:
            key, value = line.split("\t")
            if len(key) > 1:
                d[key] = max(0.0, float(value))
    dic[kenmei] = d
    fin.close()
    # print(len(dic["hokkaido"].keys()))
    # print(len(dic["miyagi"].keys()))
    # print(len(dic["tokyo"].keys()))
    # print(len(dic["aichi"].keys()))
    # print(len(dic["osaka"].keys()))
    # print(len(dic["hiroshima"].keys()))
    # print(len(dic["ehime"].keys()))
    # print(len(dic["hukuoka"].keys()))
    return dic

def load_labels_tweets():
    labels = list()
    tweets = list()
    speechs = list()
    gender_tags = list()
    if sys.argv[3] == "acc":
        fin = open("2tag.txt", "r")
        for line in fin:
            try:
                tagtag, speech, response = line.split("\t")
                tag1, tag2 = tagtag.split(" ")
            except:
                continue
            labels.append(tag1)
            tweets.append(response)
    else:
        fin = open(sys.argv[3], "r")
        for line in fin:
            try:
                tag, speech, response = line.split("\t")
            except:
                continue
            tweets.append(response)
            labels.append("<日本>") # labelsは空ではだめだけど地域を入れてはいけないので存在しないタグでも適当に入れておく
            gender_tags.append(tag)
            speechs.append(speech)
    fin.close()
    return labels, tweets, gender_tags, speechs

def tokenize(tweet, model):
    tweet = " ".join(model.encode(tweet, out_type=str))
    return tweet.split(" ")
    # if tweet.startswith("年末"):
    #     return ["年末", "に", "注文", "した", "M1", "の", "MacBook Pro", "が", "まだ", "届い", "て", "いない", "ん", "だが", "…"]
    # if tweet.startswith("今朝"):
    #     return ["今朝", "の", "目覚まし", "聞こえ", "なかっ", "た", "の", "は", "焦っ", "た", "（", "日頃", "の", "行い", "良", "すぎる", "ので", "間に合っ", "た", "のは", "間に合っ", "た"]
    # if tweet.startswith("初めて"):
    #     return ["初めて", "2桁", "本", "を", "投稿", "して", "、", "締切", "後", "たまらず", "寝て", "まし", "た", "。", "みんな", "沖縄", "楽しん", "で", "きて", "くれ", "〜"]
    # if tweet.startswith("外仕事"):
    #     return ["外仕事", "じゃけえ", "糖分", "が", "いる", "じゃろう", "と", "、", "会社", "の", "ボス", "が", "いちご", "大福", "を", "買っ", "て", "きて", "くれ", "まし", "た", "。"]

def average(scores):
    if len(scores) == 0:
        return 0.0
    return sum(scores) / len(scores)

def search_max_ken(words, dic, kens, tags):
    return tags[np.argmax([max([dic[ken][word] for word in words]) for ken in kens])]

def search_ave_ken(words, dic, kens, tags):
    return tags[np.argmax([average([dic[ken][word] for word in words if dic[ken][word] > 0.0]) for ken in kens])]

def calc_acc(labels, pred_tags):
    count = 0
    for label, tag in zip(labels, pred_tags):
        if label == tag:
            count += 1
    return count / len(labels)

def calc_acc_allTokyo(labels):
    count = 0
    for label in labels:
        if label == "<東京>":
            count += 1
    return count / len(labels)

def print_acc(labels, pred_tags):
    acc = calc_acc(labels, pred_tags)
    tokyo_acc = calc_acc_allTokyo(labels)
    print("acc = %.3f" % acc)
    print("tokyo_acc = %.3f" % tokyo_acc)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("usage: python %s {max, ave} {pmi, localpmi, tfidf} {acc, [filename]}" % sys.argv[0])
        sys.exit()
    kens = ["hokkaido", "miyagi", "tokyo", "aichi", "osaka", "hiroshima", "ehime", "hukuoka"]
    tags = ["<北海道>", "<宮城>", "<東京>", "<愛知>", "<大阪>", "<広島>", "<愛媛>", "<福岡>"]
    model = spm.SentencePieceProcessor(model_file="PMIsentencepiece.model")
    dic = make_dic()
    labels, tweets, gender_tags, speechs = load_labels_tweets()
    f = open("tag-%s-%s-gen-local.txt" % (sys.argv[1], sys.argv[2]), "w")
    pred_tags = list()
    for tweet, label, gender_tag, speech in tqdm(zip(tweets, labels, gender_tags, speechs)):
        words = tokenize(tweet, model)
        if sys.argv[1] == "max":
            tag = search_max_ken(words, dic, kens, tags)
        elif sys.argv[1] == "ave":
            tag = search_ave_ken(words, dic, kens, tags)
        else:
            print("usage: python %s {max, ave} {pmi, localpmi, tfidf} {acc, [filename]}" % sys.argv[0])
            sys.exit()
        pred_tags.append(tag)
        f.write(tag + " " + gender_tag + "\t" + speech + "\t" + tweet)
    f.close()
    if sys.argv[3] == "acc":
        print_acc(labels, pred_tags)