import del_emoji_sentence
import apply_spm_sentence
import detok_spm_sentence
import subprocess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot

# src = input("発話を入力してください\n")

# src = del_emoji_sentence.del_auxiliary_symbol_by_file(src)

# print(apply_spm_sentence.main(src))

# with open("/home/miyata/pbl/code/python/in_sentence.txt", "w") as f:
#     f.write(apply_spm_sentence.main(src))

# subprocess.run(['sh', '/home/miyata/pbl/code/python/pbl_shell.sh', src])

# print(detok_spm_sentence.main())


# 対話システム部分
class EchoSystem:
    def __init__(self):
        pass
 
    def initial_message(self, input):
        return {'utt': '発話を入力してください', 'end':False} 

    def reply(self, input):
        src = input['utt']
        src = del_emoji_sentence.del_auxiliary_symbol_by_file(src)
        if src == "":
            return {'utt': "タグの数が違います", 'end':False}
        with open("/home/miyata/pbl/code/python/in_sentence.txt", "w") as f:
            f.write(apply_spm_sentence.main(src))
        subprocess.run(['sh', '/home/miyata/pbl/code/python/pbl_shell.sh', src])
        tgt = detok_spm_sentence.main()
        return {'utt': tgt, 'end':False}
 
 
if __name__ == '__main__':
    system = EchoSystem()
    bot = TelegramBot(system)
    bot.run()

