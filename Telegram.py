#!/usr/bin/python3

from zmqDealer import zmqDealer
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
from Config import TOKEN
import threading
import ast

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
        print("Telegram out: ", str(update))
        self.node.send([str(update)])
        
    def callbackin(self):
        while True:
            data = self.node.receive()
            print("Telegram in: ", data)
            update = ast.literal_eval(data[-2])
            text = data[-1]
            self.updater.send_message(update["message"]["chat"]["id"], text)
        
        
class FilterNull(BaseFilter):
    def filter(self, message):
        return True
        
if __name__ == "__main__":
    Telegram(TOKEN, "telegram")
