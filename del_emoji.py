import nagisa
import emoji
import tqdm
import re
import sys

def date_to_tag(src):
    """
    日付をDATEに置き換える。
    Parameters
    ----------
    src : String
        置き換える対象の文字列
    Returns
    -------
    src : String
        置き換えた後の文字列
    """
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
    """
    絵文字をunicodeベース、顔文字をrecurrent neural networkに基づいてで削除
    （顔文字は精度そこそこ）
    Parameters
    ----------
    src : String
        削除対象の文字列
    Returns
    -------
    src : String
        削除後の文字列
    """
    src = emoji.replace_emoji(src, replace='')

    return "".join(nagisa.filter(src, filter_postags=['補助記号']).words)

def del_auxiliary_symbol_by_file(file_path):
    """
    テキストファイルに対して日付をDATEに置き換えた後に顔文字及び絵文字を削除
    Parameters
    ----------
    file_path : String
        置き換える対象の文字列が保存されたファイルのパス
    """

    with open(file_path, "r") as fin:
        with open(file_path.replace(".txt", ".demoji.txt"), "w") as fout:
            for line in tqdm.tqdm(fin):
                line = date_to_tag(line)
                tag, speech, response = line.split("\t")

                # 不自然な空白が生じるため(おそらく改行部分)、"。"に置換
                fout.write(tag + "\t" + del_auxiliary_symbol(speech).replace("　", "。") + "\t" + del_auxiliary_symbol(response).replace("　", "。") + "\n") 

#del_auxiliary_symbol_by_file(sys.argv[1])