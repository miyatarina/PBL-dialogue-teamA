import random
import tqdm
import os

def rand_ints_nodup(a, b, k):
  ns = []
  while len(ns) < k:
    n = random.randint(a, b)
    if not n in ns:
      ns.append(n)
  return ns

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

filesize = os.path.getsize("pre_data.txt")
speech_list =[]
response_list = []

with open('pre_data.txt', "r", encoding='utf-8') as fin:
    read_size = 0
    with tqdm.tqdm(total=filesize) as pbar:
        for line in fin:
            try:
                speech, response = line.strip().split("\t")
            except:
                continue
            if is_space(speech) or is_space(response):
                continue
            if count_min_word(speech, response) < opt.min_word:
                continue
            speech_list.append(speech)
            response_list.append(response)
            read_size += len(line.encode('utf-8'))
            pbar.update(read_size)

with open("100m.txt", "w", encoding='utf-8') as fout:
    for i in tqdm.tqdm(rand_ints_nodup(0, len(speech_list), 1000000)):
        fout.write(speech[i] + '\t' + response_list[i]) 
