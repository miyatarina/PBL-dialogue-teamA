import tweepy
import random
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sf',  type=str, help='save file help')

opt = parser.parse_args()

all_screen_names = set()

while True:
    # ここに先程取得したAPIキーとトークンを入力
    api_key = "oMX1HeZ3YrObHgEJ0BFTbyuJ5"
    api_secret_key = "oeS4xCPPDbW5aHYZYIrnosgnaixuta53Vs9hBaRORYZIXnqwWp"
    access_token = "1271122693673238528-1kP4JVsDIULKS0vDSD0PwPQpr9Wxar"
    access_token_secret = "LnDhvzpSfsMS84OSEiFTUD5GWqu4yjjOcLSohTaBPfLrB"

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth_handler=auth, wait_on_rate_limit=True)

    # botのツイートを除外するため，一般的なクライアント名を列挙
    sources = ["TweetDeck", "Twitter Web Client", "Twitter for iPhone",
               "Twitter for iPad", "Twitter for Android", "Twitter for Android Tablets",
               "ついっぷる", "Janetter", "twicca", "Keitai Web", "Twitter for Mac"]
    

    screen_names = set()
    words = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん")
    for s in api.search(q=random.choice(words), \
                        lang='ja', \
                        result_type='mixed', \
                        tweet_fields=['author_id'], \
                        count=100000, \
                        tweet_mode='extended'):
                        # q : 検索文字列
                        # lang='ja' : 日本語のツイートのみ\を取得
                        # tweet_mode = 'extended' : 省略されたツイートを全て取得

        if s.source in sources: 
            screen_names.add(s.author.screen_name)
            user = api.get_user(screen_name=s.author.screen_name)
            user_description = user.description
            if re.compile(r'.*(^(義理の|義|祖).*父)|(^(長|次|三|四|老若).*男).*').search(user_description):
                    if not s.author.screen_name in all_screen_names:
                        screen_names.add(s.author.screen_name)
                        all_screen_names.add(s.author.screen_name)

    # ステータスidからステータスを得るためのdict
    id2status = {}

    # スクリーンネームからタイムラインを取得してツイートを保存．
    # さらにリプライツイートであれば，リプライ先のスクリーンネームも取得
    in_reply_to_screen_names = set()
    for name in screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=200):
                # リンクもしくはハッシュタグを含むツイートは除外する
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
                    if s.in_reply_to_screen_name is not None : # リプライ先のスクリーンネームがあれば
                        if s.in_reply_to_screen_name not in screen_names: # リプライ先のスクリーンネームが screen_names に入ってなければ
                            in_reply_to_screen_names.add(s.in_reply_to_screen_name)
                                
        except Exception as e:
            continue

    # リプライ先のスクリーンネームからタイムラインを取得してツイートを保存
    for name in in_reply_to_screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=200):
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
        except Exception as e:
            continue

    # 保存したツイートのリプライ先のツイートが保存されていれば，id2replyidのキーを元ツイートのid，値をリプライ先ツイートのidとする
    id2replyid = {}
    for _, s in id2status.items():
        if s.in_reply_to_status_id in id2status:
            id2replyid[s.in_reply_to_status_id] = s.id


    # id2replyidのkey valueからstatusを取得し，ツイートペアをタブ区切りで保存
    with open(opt.sf, "a") as f:
        for id, rid in id2replyid.items():

            tag = "<男>"

            # 改行は半角スペースに置換
            tweet1 = id2status[id].full_text.replace("\n", " ")
            # スクリーンネームを正規表現を用いて削除
            tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

            tweet2 = id2status[rid].full_text.replace("\n", " ")
            tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

            f.write(tweet1 + "\t" + tweet2 + "\t" + tag + "\n")
    
    print("Write " + str(len(id2replyid)) + " pairs.")

