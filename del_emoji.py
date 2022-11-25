import emoji
import nagisa

def del_emoji(src):
    return emoji.replace_emoji(src, replace='')

def del_URLEmoticon(src):
    return nagisa.filter(src, filter_postags=['補助記号', 'URL']).words

def tokenize_del(src):
    src = emoji.replace_emoji(src, replace='')
    return nagisa.filter(src, filter_postags=['補助記号', 'URL']).words