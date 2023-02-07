## 学習
1. `honban.sh`の`input_file`に学習用データを指定する．
1. `spm`には，`get_sentencepiece.py`から出力されるモデル名を指定する．（ここでは`test.model`）
1. `train_n`に学習用データの数を指定する．
1. `valid_n`に検証用データの数を指定する．
1. `test_n`に評価用データの数を指定する．
1. 最後に，
```bash
bash honban.sh
```
で`honban.sh`を実行する．

## Telegramとの接続
```bash
python seq_steps.py
```
で`seq_steps.py`を実行する．

`seq_steps.py`内で使用する`telegram_bot.py`については[こちら](https://github.com/dsbook/dsbook/blob/master/telegram_bot.py)のものを用いた．

## Telegramでの対話
入力は
```bash
入力文 ||| <地域タグ> <性別タグ>
```
で行う．

地域タグとして指定できるものは，北海道，宮城，東京，愛知，大阪，広島，愛媛，福岡

性別タグとして指定できるものは，男性，女性である．