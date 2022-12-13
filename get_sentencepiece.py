#https://github.com/google/sentencepiece/blob/master/doc/options.md
import sentencepiece as spm
import sys

tag_list = []

# 学習の実行
def sentence_piece_train(file_path):
    """
    モデルの学習

    Parameters
    ----------
    file_path : str
        学習対象のテキスト
    
    Note
    ----------
        学習テキストはtag\tspeech\tresponse\nが前提
        tagは事前に追加、学習データからは除去
    """
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
