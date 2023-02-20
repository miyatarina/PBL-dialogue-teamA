import tweepy
import random
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-sf',  type=str, help='save file help')

opt = parser.parse_args()

all_screen_names = set() #重複を判断のための集合

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
    # ひらがな一文字で検索し，スクリーンネームを取得
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
            #print(s.author.screen_name)
            try:
                user = api.get_user(screen_name=s.author.screen_name)
            except tweepy.error.TweepError:
                print("User has been suspended. or User not found.")
                continue

            user_location = user.location
            user_description = user.description
            
            if s.author.screen_name not in all_screen_names and re.compile(r'.*(北海道|宮城|東京|愛知|大阪|広島|愛媛|福岡).*').search(user_location) and re.compile(r'.*(男|女).*').search(user_description): 
                # print(user_location)
                # print(user_description)
                # print('\n')
                screen_names.add(s.author.screen_name)
                all_screen_names.add(s.author.screen_name)
            

    # ステータスidからステータスを得るためのdict
    id2status = {}

    # スクリーンネームからタイムラインを取得してツイートを保存．
    # さらにリプライツイートであれば，リプライ先のスクリーンネームも取得
    in_reply_to_screen_names = set()
    for name in screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=100000):
                # リンクもしくはハッシュタグを含むツイートは除外する
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
                    if s.in_reply_to_screen_name is not None:
                        if s.in_reply_to_screen_name not in screen_names:
                            in_reply_to_screen_names.add(s.in_reply_to_screen_name)
        except Exception as e:
            continue

    # リプライ先のスクリーンネームからタイムラインを取得してツイートを保存
    for name in in_reply_to_screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=100000):
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
        except Exception as e:
            continue

    


    # id2replyidのkey valueからstatusを取得し，ツイートペアをタブ区切りで保存
    def writefile(id, rid):
        with open(opt.sf, "a") as f:
            user_location = api.get_user(screen_name=s.author.screen_name).location
            if re.compile(r'.*(北海道).*').search(user_location):
                tag = "<北海道>"
            elif re.compile(r'.*(宮城).*').search(user_location):
                tag = "<宮城>"
            elif re.compile(r'.*(東京).*').search(user_location):
                tag = "<東京>"
            elif re.compile(r'.*(愛知).*').search(user_location):
                tag = "<愛知>"
            elif re.compile(r'.*(大阪).*').search(user_location):
                tag = "<大阪>"
            elif re.compile(r'.*(広島).*').search(user_location):
                tag = "<広島>"
            elif re.compile(r'.*(愛媛).*').search(user_location):
                tag = "<愛媛>"
            elif re.compile(r'.*(福岡).*').search(user_location):
                tag = "<福岡>"
            else:
                return
            
            # 性別
            user_description = api.get_user(screen_name=s.author.screen_name).description
            if re.compile(r'.*(男).*').search(user_description):
                tag2 = "<男>"
            elif re.compile(r'.*(女).*').search(user_description):
                tag2 = "<女>"
            else:
                return
              

            # 改行は半角スペースに置換
            tweet1 = id2status[id].full_text.replace("\n", " ")
            # スクリーンネームを正規表現を用いて削除
            tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

            tweet2 = id2status[rid].full_text.replace("\n", " ")
            tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

            f.write(tag + ' ' + tag2 + "\t" + tweet1+ "\t" + tweet2 + "\n")
      
    # 保存したツイートのリプライ先のツイートが保存されていれば，id2replyidのキーを元ツイートのid，値をリプライ先ツイートのidとする
    id2replyid = {}
    for _, s in id2status.items():
        if s.in_reply_to_status_id in id2status:
            if s.in_reply_to_status_id != s.id:
                id2replyid[s.in_reply_to_status_id] = s.id
                writefile(s.id, s.in_reply_to_status_id)
    print("Write " + str(len(id2replyid)) + " pairs.")


    # ツイート3組をタブ区切りで保存
    # f = open("tweet_triples.txt", "a")
    # for id, rid in id2replyid.items():
    #     if rid in id2replyid:
    #         tweet1 = id2status[id].full_text.replace("\n", " ")
    #         tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

    #         tweet2 = id2status[rid].full_text.replace("\n", " ")
    #         tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

    #         tweet3 =  id2status[id2replyid[rid]].full_text.replace("\n", " ")
    #         tweet3 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet3)
    #         f.write(tweet1 + " SEP " + tweet2 + "\t" + tweet3 + "\n")
    # f.close()
