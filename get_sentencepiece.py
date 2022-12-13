#https://github.com/google/sentencepiece/blob/master/doc/options.md
import sentencepiece as spm
import sys

tag_list = ['<タグ>','<male>', '<female>']

# 学習の実行
def sentence_piece_train(file_path):
    with open(file_path, "r", encoding="utf-8") as fin:
        with open(file_path.replace(".txt", ".detab.txt"), "w", encoding="utf-8") as fout:
            for line in fin:
                tag, speech, response = line.split("\t")
                fout.write(speech + "\n" + response) 

    spm.SentencePieceTrainer.train(
    input=file_path.replace(".txt", ".detab.txt"), 
    model_prefix='test', 
    vocab_size=8000, 
    character_coverage=0.9995,
    user_defined_symbols = tag_list
    )

sentence_piece_train(sys.argv[1])