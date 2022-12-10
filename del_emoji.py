import nagisa
import emoji
import re

def date_to_tag(src):
    pattern = r'\d{4}/\d{2}/\d{2}(（|\()(月|火|水|木|金|土|日)(）|\))'
    src = re.sub(pattern, 'DATE', src)
    pattern = r'\d{2}/\d{2}(（|\()(月|火|水|木|金|土|日)(）|\))'
    src = re.sub(pattern, 'DATE', src)
    pattern = r'\d{4}/\d{2}/\d{2}'
    src = re.sub(pattern, 'DATE', src)
    pattern = r'/\d{2}/\d{2}'
    src = re.sub(pattern, 'DATE', src)
    return src


def del_auxiliary_symbol(src):
    src = emoji.replace_emoji(src, replace='')

    return "".join(nagisa.filter(src, filter_postags=['補助記号']).words)

def del_specific_symbol(src):
    pattern = re.compile(r'.*\([^あ-ん\u30A1-\u30F4\u2E80-\u2FDF\u3005-\u3007\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002EBEF]+?\).*')

    src = re.sub(pattern, '', src)

    return src



def del_auxiliary_symbol_by_file(file_path):
    fout = open(file_path.replace(".txt", ".tok.txt"), "w")
    fin = open(file_path, "r")
    for line in fin:
        line = date_to_tag(line)
        line = del_auxiliary_symbol(line)
        fout.write(del_specific_symbol(line) + "\n")
    fin.close()
    fout.close()
