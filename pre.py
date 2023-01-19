import random
import os

def is_space(text):
    if " " in text or "　" in text:
        return True
    else:
        return False

def count_min_word(text, text_pair):
    text_count = len(text)
    text_pair_count = len(text_pair)
    if text_count < text_pair_count:
        return text_count
    else:
        return text_pair_count

def rand_ints_nodup(a, b, k):
  ns = []
  while len(ns) < k:
    n = random.randint(a, b)
    if not n in ns:
        print(len(ns))
        ns.append(n)
  return ns

speech_list =[]
response_list = []

with open("pre_data.txt", "r", encoding='utf-8') as fin:
        for line in fin:
            try:
                speech, response = line.strip().split("\t")
            except:
                continue
            if is_space(speech) or is_space(response):
                continue
            if count_min_word(speech, response) < 10:
                continue
            speech_list.append(speech)
            response_list.append(response)

with open("100m.txt", "w", encoding='utf-8') as fout:
    for i in rand_ints_nodup(0, len(speech_list), 1000000):
        fout.write(speech[i] + '\t' + response_list[i]) 
