#!/usr/bin/python3

from zmqDealer import zmqDealer
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
from Config import TOKEN
import threading
import ast
import traceback

class Telegram:
    def __init__(self, token, identity):
        self.node = zmqDealer(identity)
        self.updater = Updater(token=token)
        self.filternull = FilterNull()
        self.updater.dispatcher.add_handler(MessageHandler(self.filternull, self.callbackout))
        threading.Thread(target=self.callbackin).start()
        self.updater.start_polling()
        self.update = False
        
    def callbackout(self, bot, update):
        try:
            updateid = update.update_id
            text = update.message.text
            self.node.send([updateid, "text", text])
            chatid = update.message.chat.id
            self.node.send([updateid, "chatid", chatid])
            fromid = update.message.from_user.id
            self.node.send([updateid, "fromid", fromid])
            admins = []
            if update.message.chat.id != update.message.from_user.id:
                for admin in self.updater.bot.get_chat_administrators(chatid):
                    admins.append(str(admin.user.id))
                admins = ",".join(admins)
                self.node.send([updateid, "admins", admins])
        except:
            traceback.print_exc()
        
    def callbackin(self):
        while True:
            data = self.node.receive()
            print("Telegram in: ", data)
            self.bot.send_message(data[-2], data[-1])
        
class FilterNull(BaseFilter):
    def filter(self, message):
        return True
        
if __name__ == "__main__":
    Telegram(TOKEN, "telegram")
