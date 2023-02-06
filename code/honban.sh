input_file=1tag_2tag_all_3M.shuf
spm=test.model
train_n=3350000
valid_n=20000
test_n=1000

# 1tag_2tag_all_3M.shuf.txt -> 3374557行

# 都道府県ごとのタグの数出すやつ
# cut -f1 1tag_response.txt | sort | uniq -c | sort -nr

# pip install OpenNMT-py==3.0.0

# miyata.txt -> miyata.demoji.txt
# ツイートのテキストから絵文字を消す
# python del_emoji.py ${input_file}.txt

# センテンスピースのモデルを学習する
# miyata.demoji.txt -> miyata.demoji.detab.txt, (test.model, test.vocab)
# 　　　　　　　　　学習用のテキスト　　　単語分割のモデル
# python get_sentencepiece.py ${input_file}.txt

# 絵文字を消したテキストを単語分割する
# miyata.demoji.txt -> miyata.demoji.tok.txt
# python apply-spm.py ${input_file}.txt $spm

# 単語分割したやつをシャッフル（男女のタグがいい感じに混ざるようにする）
# shuf ${input_file}.demoji.tok.txt > ${input_file}.shuf.demoji.tok.txt

# OpenNMT読み込むようにsrcとtgtに分ける
# cut -f1,2 ${input_file}.tok.txt | tr "\t" " " > ${input_file}.tok.src.txt
# cut -f3 ${input_file}.tok.txt > ${input_file}.tok.tgt.txt

# # devを作る
# tail -${valid_n} ${input_file}.tok.src.txt > ${input_file}.tok.src.valid.txt
# tail -${valid_n} ${input_file}.tok.tgt.txt > ${input_file}.tok.tgt.valid.txt

# # trainを作る
# head -${train_n} ${input_file}.tok.src.txt > ${input_file}.tok.src.train.txt
# head -${train_n} ${input_file}.tok.tgt.txt > ${input_file}.tok.tgt.train.txt

# # testを作る
# head -$(( $train_n+$test_n )) ${input_file}.tok.src.txt | tail -${test_n} > ${input_file}.tok.src.test.txt
# head -$(( $train_n+$test_n )) ${input_file}.tok.tgt.txt | tail -${test_n} > ${input_file}.tok.tgt.test.txt

# ONMT用の前処理
onmt_build_vocab -config "transformer.yaml" -n_sample $train_n -overwrite

# ONMT用の学習
onmt_train -config "transformer.yaml"

curl -X POST -H 'Content-type: application/json' --data '{"text":"transformer学習終わったよ"}' https://hooks.slack.com/services/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
