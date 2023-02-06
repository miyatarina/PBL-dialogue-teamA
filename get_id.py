import sentencepiece as spm

class LearningData:
    def __init__(self, file_path, model):
        """
        コンストラクタ

        Parameters
        ----------
        file_path : str
            処理対象のファイルパス

        model : str
            処理に使うモデルのファイルパス

        Notes
        -----
            処理対象のファイルは
                tag\tspeech\tresponse\n
            である前提
        """
        self.sp = spm.SentencePieceProcessor()
        self.sp.load(model)

        self.tag_list = []
        self.speech_list = []
        self.response_list = []

        with open(file_path, "r", encoding='utf-8') as f:
            for line in f:
                tag, speech, response = line.split("\t")
                self.tag_list.append(self.sp.EncodeAsPieces(tag))
                self.speech_list.append(self.sp.EncodeAsPieces(speech))
                self.response_list.append(self.sp.EncodeAsPieces(response))
    
    def get_tag_list(self):
        """
        変換したタグのリストを返す。
        """
        return self.tag_list

    def get_speech_list(self):
        """
        変換したspeechのリストを返す。
        """
        return self.speech_list

    def get_response_list(self):
        """
        変換したresponseのリストを返す。
        """
        return self.response_list
    
    def get_length(self):
        """
        変換したタグ数を返す。
        """
        return len(self.tag_list)

'''
print("---------test---------")
ld = LearningData("miyata.demoji.txt", "test.model")

print("---------len_test---------")
print(ld.get_length())

print("---------tag_test---------")
for i in range(0, 10):
    print(ld.get_tag_list()[i])

print("---------speech_test---------")
for i in range(0, 10):
    print(ld.get_speech_list()[i])

print("---------response_test---------")
for i in range(0, 10):
    print(ld.get_response_list()[i])
'''