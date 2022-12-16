#収集する都道府県に応じてファイル名を置き換えてください
SAVE_FILE="tweet_pairs_都道府県名.txt"

python python/collect_testdata.py -sf $SAVE_FILE
