# 学習

1. honban.shのinput_fileに学習用データを指定する
1. spmには，get_sentencepiece.pyから出力されるモデル名を指定する（ここではtest.model）
1. train_nに学習用データの数を指定する
1. valid_nに検証用データの数を指定する
1. test_nに評価用データの数を指定する
1. 最後に，
```bash
bash honban.sh
```
を行う