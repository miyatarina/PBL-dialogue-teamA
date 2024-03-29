## 環境構築
```
conda create [環境名] python=3.8 anaconda
```
によって環境構築を行う．
<!-- 環境名：git_pbl -->

さらに，
```
pip3 install tweepy==3.8.0 urllib3==1.26.9
```
を実行してデータ収集に必要なモジュールをインストールする．

## 性別タグ付きデータの収集
性別タグのついた発話文・応答文のペアをTwitterAPIによって収集する．

プログラムの実行は、スクリプトによって行う．
具体的には、次のようなコマンドでプログラムを実行できる．
性別によって実行ファイルが異なるため，以下の2文を実行する．
```
bash mycollect_gen_man.sh [出力ファイルパス]
bash mycollect_gen_woman.sh [出力ファイルパス]
```

## タグなしデータの収集


## テストデータの収集
都道府県と性別のタグが付いた発話文・応答文のペアをTwitterAPIによって収集する．
今回は北海道，宮城，東京，愛知，大阪，広島，愛媛，福岡の8都道府県で収集を行なっているが，別の都道府県で収集を行いたい場合は適宜収集したい都道府県に正規表現を置き換えて実行する．

<!-- 初回のみ以下のコードを実行して、必要なモジュールをインストールする（初回のみ）
```
pip3 install tweepy==3.8.0 urllib3==1.26.9
``` -->

プログラムの実行は、スクリプトによって行う．
具体的には、次のようなコマンドでプログラムを実行できる．
```
bash collect_testdata.sh [出力ファイルパス]
```


## 性別タグのついたデータの前処理
前処理の具体的な内容としては，絵文字・顔文字を除去するというものである．

```
python del_emoji.py [ファイル名]
```
このように記述することで，入力ファイルの前処理を行うことができる．

この際入力ファイルの記述形式は以下の通りである．
1つのタグと発話文と応答文がそれぞれタブで区切られたものを使用する．
```
<性別タグ>\t発話文\t応答文
```

## タグなしデータの前処理
前処理の具体的な内容としては，全角もしくは半角スペースの含まれる文対を除外するというものである．

ちなみにタグなしデータの前処理に使用する`pre.py`の27〜30行目のコメントアウト部分を外すと，10文字以下の分を含む文対を除外することができる．

```
python pre.py [入力ファイル]
```
このように記述することで，入力ファイルの前処理を行うことができる．

この際入力ファイルの記述形式は以下の通りである．
発話文と応答文がタグで区切られたものを使用する．
```
発話文\t応答文
```

## 地域タグの自動付与
発話文，応答文のみのタグなしデータにタグをつけたい場合は`tag_acc.py`を用いる．

この際入力ファイルの記述形式は以下の通りである．
```
発話文\t応答文
```

また，既に性別タグがついている1タグのデータにタグをつけたい場合は`tag_acc_in_gendertag.py`を用いる．

この際入力ファイルの記述形式は以下の通りである．
```
<性別タグ>\t発話文\t応答文
```

例）PMIの平均からタグづけを行いたい場合
```
python tag_acc.py ave pmi [ファイル名]
```

第一引数を`max`と指定すると最大値を用いてタグづけをする．

また，第二引数を`localpmi`と指定するとLocalPMIを用いてタグづけを行い，`tfidf`と指定するとTFIDFを用いてタグづけをする．

また，\[ファイル名\]の部分を`acc`に変更すると，タグづけの正解率を表示させることができる．

この際，`tag_acc.py`の49行目にある`2tag.txt`を以下のような形式で書かれたテキストファイルに適宜変更する．

```
<地域タグ>\s<性別タグ>\t発話文\t応答文
```

タグの間はスペース，タグと発話文もしくは発話文と応答文の間はタブで区切られている．

ちなみに，一番性能が良かったのはLocalPMIの平均値でタグづけを行なった場合である．

## 学習
1. `honban.sh`の`input_file`に入力データ（タグと応答がタブで区切られた形式)を指定する．
1. `spm`には，`get_sentencepiece.py`から出力されるモデル名を指定する．（ここでは`test.model`）
1. `train_n`に学習用データの数を指定する．
1. `valid_n`に検証用データの数を指定する．
1. `test_n`に評価用データの数を指定する．
1. 最後に，
```
bash honban.sh
```
で`honban.sh`を実行する．

ここで入力データとは，地域タグのみがついた発話応答文のペア，性別タグのみがついた発話応答文のペア，そして地域と性別タグの両方がついた発話応答文のペアを1つのファイルにまとめたものである．

ファイルの記述形式は以下の通りである．

地域/性別タグのみがついた発話応答文のペア
```
<地域/性別タグ>\t発話文\t応答文
```

地域タグと性別タグの両方がついた発話応答文のペア
```
<地域タグ>\s<性別タグ>\t発話文\t応答文
```


## 評価
1. `honban2.sh`の`pt`に使用したいモデルを指定する．
1. `input_file`に評価用データを指定する．
1. `output_file`に出力応答文を保存するファイルを指定する．
1. `correct_file`に正解応答文が書かれたファイルを指定する．
1. 最後に，
```
bash honban2.sh
```
で`honban2.sh`を実行する．

ここで，`input_file`に使用する評価用データは，`honban.sh`で作成された評価用データを使用する．


## Telegramとの接続
1. `pbl_shell.sh`のモデルのパスを先ほど評価の時に使用したモデルのものに変更する．
1. その後，
```
python seq_steps.py
```
で`seq_steps.py`を実行する．

ここで，`seq_steps.py`内で使用する`telegram_bot.py`については[こちら](https://github.com/dsbook/dsbook/blob/master/telegram_bot.py)のものを用いた．

## Telegramでの対話
入力は
```
<地域タグ>\s<性別タグ>\s発話文
```
で行う．この際入力するタグは1つでも問題ない．

地域タグとして指定できるものは，\[北海道，宮城，東京，愛知，大阪，広島，愛媛，福岡\]

性別タグとして指定できるものは，\[男性，女性\]である．