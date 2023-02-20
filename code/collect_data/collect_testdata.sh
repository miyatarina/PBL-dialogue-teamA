#収集する都道府県に応じてファイル名を置き換えてください
# SAVE_FILE="tweet_pairs_都道府県名.txt"

# python python/collect_testdata.py -sf $SAVE_FILE

# ↓ここから編集
# パス名を置き換えてください
SAVE_FILE=$1
if [ -z "$SAVE_FILE" ]; then
    echo "入力方法:bash collect_testdata.sh [出力させたいファイルパス]"
    exit 0
fi
echo "出力ファイルパス:${SAVE_FILE}"
python collect_testdata.py -sf "${SAVE_FILE}"
