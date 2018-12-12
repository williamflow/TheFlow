#!/usr/bin/python3

from zmqDealer import zmqDealer
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
import threading
import ast
import traceback
from Database import Database
from Config import HOST, USER, PASSWD, DATABASE, TGCONN, TGCHATS, TOKEN, TGIDENTITY
import Flowctl

class Telegram:
    def __init__(self, host, user, passwd, database, conntable, chattable, token, identity):
        self.identity = identity
        self.database = Database(host, user, passwd, database)
        self.conntable = conntable
        self.chattable = chattable
        self.node = zmqDealer(identity)
        self.updater = Updater(token=token)
        self.bot = self.updater.bot
        self.filternull = FilterNull()
        self.updater.dispatcher.add_handler(MessageHandler(self.filternull, self.callbackout))
        threading.Thread(target=self.callbackin).start()
        self.updater.start_polling()
        
    def callbackout(self, bot, update):
        try:
            text = update.message.text.split(" ")
            chatid = update.message.chat.id
            fromid = update.message.from_user.id
            if len(text) == 1:
                if text[0] == "/start":
                    self.send(chatid, "Please specify a name for this chat")
                if text[0] == "/listconnections":
                    if chatid == fromid:
                        chats = self.getChats(fromid)
                        ret = ""
                        for chatout, nodeout, chatin, nodein in self.database.select(self.conntable, "chatout", "nodeout", "chatin", "nodein"):
                            if chatout in chats and chatin in chats:
                                ret = ret + chats[chatout]+"."+nodeout+" "+chats[chatin]+"."+nodein+"\n"
                        if ret == "":
                            ret = "There are no connections"
                        self.send(chatid, ret)
                    else:
                        self.send(chatid, "Command avaible in private chat only")
                else:
                    self.flow(update)
            elif len(text) == 2:
                if text[0] == "/start":
                    if fromid == chatid:
                        self.send(chatid, "Command avaible only in group chats")
                    elif fromid not in [x.user.id for x in self.bot.get_chat_administrators(chatid)]:
                        self.send(chatid, "Only admins can use this command")
                    elif text[1] in self.database.select(self.chattable, "name", admin=fromid):
                        self.send(chatid, "This name has already been used")
                    elif chatid in self.database.select(self.chattable, "chat", admin=fromid):
                        self.send(chatid, "This chat is already in the Flow!")
                    else:
                        self.database.insert(self.chattable, chat=chatid, name=text[1], admin=fromid)
                        self.send(chatid, "You joined the Flow!")
                else:
                    self.flow(update)
            elif len(text) == 3:
                if text[0] == "/connect":
                    chats = self.getChats(fromid)
                    chatout, nodeout, idout = self.parseNode(text[1], chats)
                    if nodeout == False:
                        self.send(chatid, "Can't find node "+text[1])
                        return False
                    chatin, nodein, idin = self.parseNode(text[2], chats)
                    if nodein == False:
                        self.send(chatid, "Can't find node "+text[2])
                        return False
                    if len(self.database.select(self.conntable, chatout=chatout, nodeout=".".join([nodeout]+idout), chatin=chatin, nodein=".".join([nodein]+idin))) == 0:
                        self.database.insert(self.conntable, chatout=chatout, nodeout=".".join([nodeout]+idout), chatin=chatin, nodein=".".join([nodein]+idin))
                        Flowctl.connect(".".join([nodeout, chatout]+idout), ".".join([nodein, chatin]+idin))
                        self.send(chatid, "Connected")
                    else:
                        self.send(chatid, "Already Connected")
                elif text[0] == "/disconnect":
                    chats = self.getChats(fromid)
                    chatout, nodeout, idout = self.parseNode(text[1], chats)
                    if nodeout == False:
                        self.send(chatid, "Can't find node "+text[1])
                        return False
                    chatin, nodein, idin = self.parseNode(text[2], chats)
                    if nodein == False:
                        self.send(chatid, "Can't find node "+text[2])
                        return False
                    self.database.delete(self.conntable, chatout=chatout, nodeout=".".join([nodeout]+idout), chatin=chatin, nodein=".".join([nodein]+idin))
                    Flowctl.disconnect(".".join([nodeout, chatout]+idout), ".".join([nodein, chatin]+idin))
                    self.send(chatid, "Disconnected")
                else:
                    self.flow(update)
            else:
                self.flow(update)
        except:
            traceback.print_exc()
        
    def flow(self, update):
        text = update.message.text
        chatid = update.message.chat.id
        print("TO FLOW: ", chatid, " text ", text)
        self.node.send([chatid, "text", text])
    
    def callbackin(self):
        while True:
            data = self.node.receive()
            if len(data) > 2:
                print("TO TG: ", data[-3:])
                if data[-2] == "send_text":
                    self.send(data[-3], data[-1])
                elif data[-2] == "send_photo":
                    self.sendphoto(data[-3], data[-1])
    
    def send(self, chatid, message):
        self.bot.send_message(int(chatid), str(message))
        
    def sendphoto(self, chatid, filename):
        try:
            self.bot.send_photo(int(chatid), open(str(filename), "rb"))
            return True
        except:
            return False
        
    def getChats(self, fromid):
        chats = {}
        for chat, name in self.database.select(self.chattable, "chat", "name", admin=fromid):
            chats[chat] = name
        return chats
    
    def parseNode(self, node, chats):
        node = node.split(".")
        if len(node) < 2:
            return False, False, False
        chatid = False
        for chat in chats:
            if chats[chat] == node[0]:
                chatid = chat
                break
        if chatid is False:
            return False, False, False
        else:
            return chatid, node[1], node[2:]
        
class FilterNull(BaseFilter):
    def filter(self, message):
        return True
        
if __name__ == "__main__":
    Telegram(HOST, USER, PASSWD, DATABASE, TGCONN, TGCHATS, TOKEN, TGIDENTITY)
