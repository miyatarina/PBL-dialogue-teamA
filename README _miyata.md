## 地域タグの自動付与
発話文，応答文のみのタグなしデータにタグをつけたい場合は`tag_acc.py`を用いる．
既に性別タグがついている1タグのデータにタグをつけたい場合は`tag_acc_in_gendertag.py`を用いる．

例）PMIの平均からタグづけを行いたい場合
```
python tag_acc.py ave pmi [ファイル名]
```

第一引数を`max`と指定すると最大値を用いてタグづけをする．

また，第二引数を`localpmi`と指定するとLocalPMIを用いてタグづけを行い，`tfidf`と指定するとTFIDFを用いてタグづけをする．

また，\[ファイル名\]の部分を`acc`に変更すると，タグづけの正解率を表示させることができる．

この際，`tag_acc.py`の49行目にある`2tag.txt`を以下のような形式で書かれたテキストファイルに適宜変更する．

```
<地域タグ> <性別タグ>   発話文  応答文
```

タグの間はスペース，タグと発話文もしくは発話文と応答文の間はタブで区切られている．

ちなみに，一番性能が良かったのはLocalPMIの平均値でタグづけを行なった場合である．

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

## 評価
1. `honban2.sh`の`pt`に使用したいモデルを指定する．
1. `input_file`に学習用データを指定する．
1. `output_file`に出力応答文を保存するファイルを指定する．
1. 最後に，
```bash
bash honban2.sh
```
で`honban2.sh`を実行する．

## Telegramとの接続
1. `pbl_shell.sh`のモデルのパスを先ほど評価の時に使用したモデルのものに変更する．
1. その後，
```bash
python seq_steps.py
```
で`seq_steps.py`を実行する．

ここで，`seq_steps.py`内で使用する`telegram_bot.py`については[こちら](https://github.com/dsbook/dsbook/blob/master/telegram_bot.py)のものを用いた．

## Telegramでの対話
入力は
```
入力文 ||| <地域タグ> <性別タグ>
```
で行う．

地域タグとして指定できるものは，\[北海道，宮城，東京，愛知，大阪，広島，愛媛，福岡\]

性別タグとして指定できるものは，\[男性，女性\]である．