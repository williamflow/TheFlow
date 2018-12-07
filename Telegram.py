#!/usr/bin/python3

from zmqDealer import zmqDealer
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, BaseFilter
import threading
import ast
import traceback
from Database import Database
from Config import *
import Flowctl

class Telegram:
    def __init__(self, token, identity):
        self.identity = identity
        self.database = Database(HOST, USER, PASSWD, DATABASETELEGRAM)
        self.node = zmqDealer(identity)
        self.updater = Updater(token=token)
        self.bot = self.updater.bot
        self.filternull = FilterNull()
        self.updater.dispatcher.add_handler(MessageHandler(self.filternull, self.callbackout))
        threading.Thread(target=self.callbackin).start()
        self.updater.start_polling()
        self.update = False
        
    def callbackout(self, bot, update):
        try:
            text = update.message.text.split(" ")
            chatid = update.message.chat.id
            fromid = update.message.from_user.id
            if len(text) == 1:
                if text[0] == "/start":
                    self.send(chatid, "Please specify a name for this chat")
                if text[0] == "/listconnections":
                    chats = self.getChats(fromid)
                    ret = ""
                    for connection in self.database.select("connection", "chatout", "nodeout", "chatin", "nodein"):
                        if connection[0] in chats and connection[2] in chats:
                            nodein = connection[1].split(".")
                            nodeout = connection[3].split(".")
                            ret = ret + chats[nodein[1]]+"."+nodein[0]+"."+".".join(nodein[2:])+" -> "+chats[nodeout[1]]+"."+nodeout[0]+"."+".".join(nodeout[2:])+"\n"
                    if ret == "":
                        ret = "There are no connections"
                    self.send(chatid, ret)
                else:
                    self.flow(update)
            elif len(text) == 2:
                if text[0] == "/start":
                    if fromid == chatid:
                        self.send(chatid, "Command avaible only in group chats")
                    elif fromid not in [x.user.id for x in self.bot.get_chat_administrators(chatid)]:
                        self.send(chatid, "Only admins can use this command")
                    elif text[1] in self.database.select("chats", "name"):
                        self.send(chatid, "This name has already been used")
                    elif chatid in self.database.select("chats", "chat"):
                        self.send(chatid, "You have already done this action")
                    else:
                        self.database.insert("chats", chat=chatid, name=text[1], admin=fromid)
                        self.send(chatid, "You joined the Flow!")
                else:
                    self.flow(update)
            elif len(text) == 3:
                if text[0] == "/connect":
                    chats = self.getChats(fromid)
                    chatout, nodeout = self.parseNode(text[1], chats)
                    if nodeout == False:
                        self.send(chatid, "Can't find chat "+text[1])
                        return False
                    chatin, nodein = self.parseNode(text[2], chats)
                    if nodein == False:
                        self.send(chatid, "Can't find chat "+text[2])
                        return False
                    self.database.insert("connection", chatout=chatout, nodeout=nodeout, chatin=chatin, nodein=nodein)
                    Flowctl.connect(nodeout, nodein)
                    self.send(chatid, "Connected")
                elif text[0] == "/disconnect":
                    chats = self.getChats(fromid)
                    chatout, nodeout = self.parseNode(text[1], chats)
                    if nodeout == False:
                        self.send(chatid, "Can't find chat "+text[1])
                        return False
                    chatin, nodein = self.parseNode(text[2], chats)
                    if nodein == False:
                        self.send(chatid, "Can't find chat "+text[2])
                        return False
                    self.database.delete("connection", chatout=chatout, nodeout=nodeout, chatin=chatin, nodein=nodein)
                    Flowctl.disconnect(nodeout, nodein)
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
        self.node.send([chatid, text])
    
    def callbackin(self):
        while True:
            data = self.node.receive()
            print(data)
            self.send(data[0], data[1])
    
    def send(self, chatid, message):
        self.bot.send_message(int(chatid), str(message))
        
    def getChats(self, fromid):
        result = self.database.select("chats", "chat", "name", admin=fromid)
        chats = {}
        for row in result:
            chats[row[0]] = row[1]
        return chats
    
    def parseNode(self, node, chats):
        node = node.split(".")
        if len(node) < 2:
            return False, False
        chatid = False
        for chat in chats:
            if chats[chat] == node[0]:
                chatid = chat
                break
        if chatid is False:
            return False, False
        else:
            return chatid, ".".join([node[1], chatid]+node[2:])
        
class FilterNull(BaseFilter):
    def filter(self, message):
        return True
        
if __name__ == "__main__":
    Telegram(TOKEN, "telegram")
