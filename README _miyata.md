## 学習

1. `honban.sh`の`input_file`に学習用データを指定する
1. `spm`には，`get_sentencepiece.py`から出力されるモデル名を指定する（ここでは`test.model`）
1. `train_n`に学習用データの数を指定する
1. `valid_n`に検証用データの数を指定する
1. `test_n`に評価用データの数を指定する
1. 最後に，
```bash
bash honban.sh
```
で`honban.sh`を実行する．

## Telegramとの接続


Telegram_bot.pyは[こちら](https://github.com/dsbook/dsbook/blob/master/telegram_bot.py)のものを用いました．