import nagisa
import emoji
import tqdm
import re
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-mw', '--min_word', type=int, default=10, help='minimum number of characters')
parser.add_argument('-ns', '--number_sentences', type=int, default=1000000, help='number of sentences to get')

def del_auxiliary_symbol(src):
    """
    絵文字をunicodeベース、顔文字をrecurrent neural networkに基づいてで削除
    （顔文字は精度そこそこ）
    Parameters
    ----------
    src : String
        削除対象の文字列
    Returns
    -------
    src : String
        削除後の文字列
    """
    src = emoji.replace_emoji(src, replace='')

    return "".join(nagisa.filter(src, filter_postags=['補助記号']).words)

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
      ns.append(n)
  return ns

def random_pair(file_path):
    """
    テキストファイルに対して日付をDATEに置き換えた後に顔文字及び絵文字を削除
    Parameters
    ----------
    file_path : String
        置き換える対象の文字列が保存されたファイルのパス
    """
    speech_list =[]
    response_list = []
    with open(file_path, "r", encoding='utf-8') as fin:
        for line in tqdm.tqdm(fin):
            try:
                speech, response = line.strip().split("\t")
            except:
                continue
            if is_space(speech) or is_space(response):
                continue
            if count_min_word(speech, response) < parser.min_word:
                continue
            speech_list.append(speech)
            response_list.append(response)
    
    with open(file_path.replace(".txt", ".demoji.txt"), "w", encoding='utf-8') as fout:
        for i in rand_ints_nodup(0, len(speech_list), parser.number_sentences):
            fout.write(del_auxiliary_symbol(speech_list[i]).replace("　", "。") + "\t" + del_auxiliary_symbol(response_list[i]).replace("　", "。") + "\n") 

random_pair(sys.argv[1])
