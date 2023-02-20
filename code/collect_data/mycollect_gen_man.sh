#SAVE_FILEを指定
# SAVE_FILE="mycollect_gen_man.txt"
# python python/mycollect_gen_man.py -sf $SAVE_FILE

# ↓ここから編集
SAVE_FILE=$1
if [ -z "$SAVE_FILE" ]; then
    echo "入力方法:bash mycollect_gen_man.sh [出力させたいファイルパス]"
    exit 0
fi
echo "出力ファイルパス:${SAVE_FILE}"
python mycollect_gen_man.py -sf "${SAVE_FILE}"