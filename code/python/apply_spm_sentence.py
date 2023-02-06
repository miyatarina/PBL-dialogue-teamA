# coding: utf-8

import sys
import sentencepiece as spm

def main(src):
    # センテンスピースのモデル読み込む
    model = spm.SentencePieceProcessor(model_file="/home/miyata/pbl/code/python/test.model")

    # 分割する
    tag, speech = src.strip().split("\t")
    speech = " ".join(model.encode(speech, out_type=str))
    return (tag + " " + speech + "\t")


if __name__ == '__main__':
    main(src)
