pt=rnn_step_81000
input_file=1tag_2tag_all_3M.shuf.tok.src.test.txt
output_file=honban_output.txt
correct_file=1tag_2tag_all_3M.shuf.tgt.src.test.txt

# 翻訳
# onmt_translate -model "onmt_data/${pt}.pt" -src "${input_file}.shuf.demoji.tok.src.test.txt" -output "pred.rnn.txt" -gpu "0" -verbose
onmt_translate -model "onmt_data/${pt}.pt" -src "${input_file}" -output "${output_file}" -gpu "0" -verbose

# 後処理
# pred.rnn.txt -> pred.rnn.detok.txt
python detok-spm.py ${output_file}

# 評価
python bleu.py ${output_file} ${correct_file}
