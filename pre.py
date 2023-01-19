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

filesize = os.path.getsize(file_path)
speech_list =[]
response_list = []

with open(file_path, "r", encoding='utf-8') as fin:
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
