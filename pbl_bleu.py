# 評価

from torchtext.data.metrics import bleu_score

def bleu(fname_ref, fname_pred):    
    # 正解文
    fin = open(fname_ref, "r")
    refs = [[line.strip().split()] for line in fin]
    fin.close()
    # 出力文
    fin = open(fname_pred, "r")
    preds = [line.strip().split() for line in fin]
    fin.close()
    # BLEU
    score = bleu_score(preds, refs)
    print("BLEU = %.2f" % (score*100))

ref_file = "outou.test.txt"
pred_file = "outou.txt"
bleu(ref_file, pred_file)

