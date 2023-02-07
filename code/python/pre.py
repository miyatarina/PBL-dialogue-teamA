import sys

def is_space(text):
    if " " in text or "　" in text:
        return True
    else:
        return False

def count_min_word(text, text_pair):
    text_count = len(text)
    text_pair_count = len(text_pair)
    if text_count < text_pair_count:
        return text_count
    else:
        return text_pair_count

def del_min_text(file_path):
    with open(file_path, "r", encoding='utf-8') as fin:
        with open("pre_data.txt", "a", encoding='utf-8') as fout:
            for line in fin:
                try:
                    speech, response = line.strip().split("\t")
                except:
                    continue
                if is_space(speech) or is_space(response):
                    continue
                '''
                if count_min_word(speech, response) < 10:
                    continue
                '''
                fout.write(speech + '\t' + response + '\n')             

del_min_text(sys.argv[1])