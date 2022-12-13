import sentencepiece as spm

# モデルの作成
sp = spm.SentencePieceProcessor()
sp.Load("test.model")


'''
print("---------test---------")

print("<male> 私は男です。")
print(sp.EncodeAsPieces("<male> 私は男です。"))
print(sp.EncodeAsIds("<male>私は男です。"))
print("<female>   私は女です。")
print(sp.EncodeAsPieces("<female>   私は女です。"))
print(sp.EncodeAsIds("<female>   私は女です。"))
'''
