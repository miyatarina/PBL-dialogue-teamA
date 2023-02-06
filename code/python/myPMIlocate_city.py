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
    
    # ひらがな一文字で検索し，スクリーンネームを取得
    words = list("あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん") 

    #五十音のいずれかを含むツイートを検索
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
            try:
                user = api.get_user(screen_name=s.author.screen_name)
            except tweepy.error.TweepError:
                print("User has been suspended. or User not found.")
                continue
            user_location = user.location
            user_description = user.description

            # プロフィール欄または位置情報欄を検索
            if s.author.screen_name not in all_screen_names:
                if re.compile(r'.*(北海道|宮城|東京|愛知|大阪|広島|愛媛|福岡|札幌|函館|小樽|室蘭|旭川|釧路|帯広|北見|夕張|岩見沢|網走|留萌|苫小牧|稚内|美唄|芦別|江別|赤平|紋別|士別|名寄|三笠|根室|千歳|滝川|砂川|歌志内|深川|富良野|登別|恵庭|伊達|北広島|石狩|北斗|仙台|石巻|塩竈|気仙沼|白石|名取|角田|多賀城|岩沼|登米|栗原|東松島|大崎|富谷|八王子|立川|武蔵野|三鷹|青梅|府中|昭島|調布|町田|小金井|小平|日野|東村山|国分寺|国立|福生|狛江|東大和|清瀬|東久留米|武蔵村山|多摩|稲城|羽村|あきる野|西東京|名古屋|豊橋|岡崎|一宮|瀬戸|半田|春日井|豊川|津島|碧南|刈谷|豊田|安城|西尾|蒲郡|犬山|常滑|江南|小牧|稲沢|新城|東海|大府|知多|知立|尾張旭|高浜|岩倉|豊明|日進|田原|愛西|清須|北名古屋|弥富|みよし|あま|長久手|大阪|堺|岸和田|豊中|池田|吹田|泉大津|高槻|貝塚|守口|枚方|茨木|八尾|泉佐野|富田林|寝屋川|河内長野|松原|大東|和泉|箕面|柏原|羽曳野|門真|摂津|高石|藤井寺|東大阪|泉南|四條畷|交野|大阪狭山|阪南|広島|呉|竹原|三原|尾道|福山|府中|三次|庄原|大竹|東広島|廿日市|安芸高田|江田島|松山|今治|宇和島|八幡浜|新居浜|西条|大洲|伊予|四国中央|西予|東温|北九州|福岡|大牟田|久留米|直方|飯塚|田川|柳川|八女|筑後|大川|行橋|豊前|中間|小郡|筑紫野|春日|大野城|宗像|太宰府|古賀|福津|うきは|宮若|嘉麻|朝倉|みやま|糸島|那珂川).*').search(user_location):
                    # print(user_location)
                    screen_names.add(s.author.screen_name)
                    all_screen_names.add(s.author.screen_name)
                elif re.compile(r'.*(北海道|宮城|東京|愛知|大阪|広島|愛媛|福岡|札幌|函館|小樽|室蘭|旭川|釧路|帯広|北見|夕張|岩見沢|網走|留萌|苫小牧|稚内|美唄|芦別|江別|赤平|紋別|士別|名寄|三笠|根室|千歳|滝川|砂川|歌志内|深川|富良野|登別|恵庭|伊達|北広島|石狩|北斗|仙台|石巻|塩竈|気仙沼|白石|名取|角田|多賀城|岩沼|登米|栗原|東松島|大崎|富谷|八王子|立川|武蔵野|三鷹|青梅|府中|昭島|調布|町田|小金井|小平|日野|東村山|国分寺|国立|福生|狛江|東大和|清瀬|東久留米|武蔵村山|多摩|稲城|羽村|あきる野|西東京|名古屋|豊橋|岡崎|一宮|瀬戸|半田|春日井|豊川|津島|碧南|刈谷|豊田|安城|西尾|蒲郡|犬山|常滑|江南|小牧|稲沢|新城|東海|大府|知多|知立|尾張旭|高浜|岩倉|豊明|日進|田原|愛西|清須|北名古屋|弥富|みよし|あま|長久手|大阪|堺|岸和田|豊中|池田|吹田|泉大津|高槻|貝塚|守口|枚方|茨木|八尾|泉佐野|富田林|寝屋川|河内長野|松原|大東|和泉|箕面|柏原|羽曳野|門真|摂津|高石|藤井寺|東大阪|泉南|四條畷|交野|大阪狭山|阪南|広島|呉|竹原|三原|尾道|福山|府中|三次|庄原|大竹|東広島|廿日市|安芸高田|江田島|松山|今治|宇和島|八幡浜|新居浜|西条|大洲|伊予|四国中央|西予|東温|北九州|福岡|大牟田|久留米|直方|飯塚|田川|柳川|八女|筑後|大川|行橋|豊前|中間|小郡|筑紫野|春日|大野城|宗像|太宰府|古賀|福津|うきは|宮若|嘉麻|朝倉|みやま|糸島|那珂川).?出身.*').search(user_description):
                    # print(user_location)
                    screen_names.add(s.author.screen_name)
                    all_screen_names.add(s.author.screen_name)


    # ステータスidからステータスを得るためのdict
    id2status = {}

    # スクリーンネームからタイムラインを取得してツイートを保存．
    # さらにリプライツイートであれば，リプライ先のスクリーンネームも取得
    in_reply_to_screen_names = set()
    for name in screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=10000):
                # リンクもしくはハッシュタグを含むツイートは除外する
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
                    if s.in_reply_to_screen_name is not None:
                        if s.in_reply_to_screen_name is not screen_names:
                            in_reply_to_screen_names.add(s.in_reply_to_screen_name)
        except Exception as e:
            continue

    # リプライ先のスクリーンネームからタイムラインを取得してツイートを保存
    for name in in_reply_to_screen_names:
        try:
            for s in api.user_timeline(name, tweet_mode='extended', count=10000):
                if "http" not in s.full_text and "#" not in s.full_text:
                    id2status[s.id] = s
                    # print(s)
        except Exception as e:
            continue

            
    def writefile(id, rid):
        # スクリーンネームからタイムラインを取得してツイートを保存． re.compile(r'.*(|大阪|広島|高知|福岡|東京|青森|沖縄|京都府).*').search(user_location)
        for name in screen_names:
            try:
                for s in api.user_timeline(name, tweet_mode='extended', count=10000):
                    # リンクもしくはハッシュタグを含むツイートは除外する
                    if "http" not in s.full_text and "#" not in s.full_text and "RT" not in s.full_text:
                        with open(opt.sf, "a") as f:

                            user_location = api.get_user(screen_name=s.author.screen_name).location
                            user_description = api.get_user(screen_name=s.author.screen_name).description
                            if re.compile(r'.*(北海道|札幌|函館|小樽|室蘭|旭川|釧路|帯広|北見|夕張|岩見沢|網走|留萌|苫小牧|稚内|美唄|芦別|江別|赤平|紋別|士別|名寄|三笠|根室|千歳|滝川|砂川|歌志内|深川|富良野|登別|恵庭|伊達|北広島|石狩|北斗).*').search(user_location) or re.compile(r'.*(北海道|札幌|函館|小樽|室蘭|旭川|釧路|帯広|北見|夕張|岩見沢|網走|留萌|苫小牧|稚内|美唄|芦別|江別|赤平|紋別|士別|名寄|三笠|根室|千歳|滝川|砂川|歌志内|深川|富良野|登別|恵庭|伊達|北広島|石狩|北斗).?出身.*').search(user_description):
                                tag = "<北海道>"
                            elif re.compile(r'.*(宮城|仙台|石巻|塩竈|気仙沼|白石|名取|角田|多賀城|岩沼|登米|栗原|東松島|大崎|富谷).*').search(user_location) or re.compile(r'.*(宮城|仙台|石巻|塩竈|気仙沼|白石|名取|角田|多賀城|岩沼|登米|栗原|東松島|大崎|富谷).?出身.*').search(user_description):
                                tag = "<宮城>"
                            elif re.compile(r'.*(東京|八王子|立川|武蔵野|三鷹|青梅|府中|昭島|調布|町田|小金井|小平|日野|東村山|国分寺|国立|福生|狛江|東大和|清瀬|東久留米|武蔵村山|多摩|稲城|羽村|あきる野|西東京).*').search(user_location) or re.compile(r'.*(東京|八王子|立川|武蔵野|三鷹|青梅|府中|昭島|調布|町田|小金井|小平|日野|東村山|国分寺|国立|福生|狛江|東大和|清瀬|東久留米|武蔵村山|多摩|稲城|羽村|あきる野|西東京).?出身.*').search(user_description):
                                tag = "<東京>"
                            elif re.compile(r'.*(愛知|名古屋|豊橋|岡崎|一宮|瀬戸|半田|春日井|豊川|津島|碧南|刈谷|豊田|安城|西尾|蒲郡|犬山|常滑|江南|小牧|稲沢|新城|東海|大府|知多|知立|尾張旭|高浜|岩倉|豊明|日進|田原|愛西|清須|北名古屋|弥富|みよし|あま|長久手).*').search(user_location) or re.compile(r'.*(愛知|名古屋|豊橋|岡崎|一宮|瀬戸|半田|春日井|豊川|津島|碧南|刈谷|豊田|安城|西尾|蒲郡|犬山|常滑|江南|小牧|稲沢|新城|東海|大府|知多|知立|尾張旭|高浜|岩倉|豊明|日進|田原|愛西|清須|北名古屋|弥富|みよし|あま|長久手).?出身.*').search(user_description):
                                tag = "<愛知>"
                            elif re.compile(r'.*(大阪|堺|岸和田|豊中|池田|吹田|泉大津|高槻|貝塚|守口|枚方|茨木|八尾|泉佐野|富田林|寝屋川|河内長野|松原|大東|和泉|箕面|柏原|羽曳野|門真|摂津|高石|藤井寺|東大阪|泉南|四條畷|交野|大阪狭山|阪南).*').search(user_location) or re.compile(r'.*(大阪|堺|岸和田|豊中|池田|吹田|泉大津|高槻|貝塚|守口|枚方|茨木|八尾|泉佐野|富田林|寝屋川|河内長野|松原|大東|和泉|箕面|柏原|羽曳野|門真|摂津|高石|藤井寺|東大阪|泉南|四條畷|交野|大阪狭山|阪南).?出身.*').search(user_description):
                                tag = "<大阪>"
                            elif re.compile(r'.*(広島|呉|竹原|三原|尾道|福山|府中|三次|庄原|大竹|東広島|廿日市|安芸高田|江田島).*').search(user_location) or re.compile(r'.*(広島|呉|竹原|三原|尾道|福山|府中|三次|庄原|大竹|東広島|廿日市|安芸高田|江田島).?出身.*').search(user_description):
                                tag = "<広島>"
                            elif re.compile(r'.*(愛媛|松山|今治|宇和島|八幡浜|新居浜|西条|大洲|伊予|四国中央|西予|東温).*').search(user_location) or re.compile(r'.*(愛媛|松山|今治|宇和島|八幡浜|新居浜|西条|大洲|伊予|四国中央|西予|東温).?出身.*').search(user_description):
                                tag = "<愛媛>"
                            elif re.compile(r'.*(福岡|北九州|福岡|大牟田|久留米|直方|飯塚|田川|柳川|八女|筑後|大川|行橋|豊前|中間|小郡|筑紫野|春日|大野城|宗像|太宰府|古賀|福津|うきは|宮若|嘉麻|朝倉|みやま|糸島|那珂川).*').search(user_location) or re.compile(r'.*(福岡|北九州|福岡|大牟田|久留米|直方|飯塚|田川|柳川|八女|筑後|大川|行橋|豊前|中間|小郡|筑紫野|春日|大野城|宗像|太宰府|古賀|福津|うきは|宮若|嘉麻|朝倉|みやま|糸島|那珂川).?出身.*').search(user_description):
                                tag = "<福岡>"

                            # 改行は半角スペースに置換
                            tweet2 = id2status[id].full_text.replace("\n", " ")
                            # スクリーンネームを正規表現を用いて削除
                            tweet2 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet1)

                            tweet1 = id2status[rid].full_text.replace("\n", " ")
                            tweet1 = re.sub(r"@[0-9a-zA-Z_]{1,15} +", "", tweet2)

                            f.write(s.author.screen_name + "\t" + tag + "\t" + tweet1+ "\t" + tweet2 + "\n")
    
            except Exception as e:
                continue


    # 保存したツイートのリプライ先のツイートが保存されていれば，id2replyidのキーを元ツイートのid，値をリプライ先ツイートのidとする
    id2replyid = {}
    for _, s in id2status.items():
        if s.in_reply_to_status_id in id2status:
            if s.in_reply_to_status_id != s.id:
                id2replyid[s.in_reply_to_status_id] = s.id
                writefile(s.id, s.in_reply_to_status_id)
    print("Write " + str(len(id2replyid)) + " pairs.")