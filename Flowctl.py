#!/usr/bin/python3

'''
    Flowctl part of TheFlow
    Copyright (C) 2018  williamflow

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import sys
from Config import *
from Database import Database
import traceback

WEBADDRESS = "tcp://*:"+PORT

def connect(nodeout, nodein):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    try:
        nodeout = parseNode(nodeout)
        nodein = parseNode(nodein)
        if len(database.select(CONNTABLE, nodeout=nodeout, nodein=nodein)) == 0:
            database.insert(CONNTABLE, nodeout=nodeout, nodein=nodein)
    except:
        print("Usage: flowctl connect node_out node_in")
        traceback.print_exc()

def disconnect(nodeout, nodein):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    try:
        nodeout = parseNode(nodeout)
        nodein = parseNode(nodein)
        database.delete(CONNTABLE, nodeout=nodeout, nodein=nodein)
    except:
        print("Usage: flowctl disconnect node_out node_in")
        traceback.print_exc()
    
def remove(node):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    try:
        node = parseNode(node)
        database.delete(CONNTABLE, nodeout=node)
        database.delete(CONNTABLE, nodein=node)
    except:
        print("Usage: flowctl remove node")
        traceback.print_exc()
    
def listconnections():
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    try:
        ret = ""
        for nodeout, nodein in database.select(CONNTABLE, "nodeout", "nodein"):
            print(nodeout+" "+nodein)
            ret = ret + nodeout+" "+nodein+"\n"
        return ret
    except:
        print("Usage flowctl listconnections")
        traceback.print_exc()
        return False
        

def parseNode(node):
    node = node.split(".")
    if node[0] == "web":
        node = [WEBADDRESS]+node[1:]
    elif node[0] == "local":
        node = [ADDRESS]+node[1:]
    else:
        node = [ADDRESS]+node
    return ".".join(node)

if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
        if cmd == "connect":
            connect(sys.argv[2], sys.argv[3])
        elif cmd == "disconnect":
            disconnect(sys.argv[2], sys.argv[3])
        elif cmd == "remove":
            remove(sys.argv[2])
        elif cmd == "listconnections":
            listconnections()
        else:
            print("Unrecognized Command")
    except:
        print("Usage: "+sys.argv[0]+" [connect|disconnect|remove|listconnections]")
