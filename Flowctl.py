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
from Config import HOST, USER, PASSWD, DATABASE, CONNTABLE
from Database import Database
import traceback

def connect(nodeout, nodein):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    if len(database.select(CONNTABLE, nodeout=nodeout, nodein=nodein)) == 0:
        database.insert(CONNTABLE, nodeout=nodeout, nodein=nodein)

def disconnect(nodeout, nodein):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    database.delete(CONNTABLE, nodeout=nodeout, nodein=nodein)
    
def remove(node):
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    database.delete(CONNTABLE, nodeout=node)
    database.delete(CONNTABLE, nodein=node)
    
def listconnections():
    database = Database(host=HOST, user=USER, passwd=PASSWD, database=DATABASE)
    ret = ""
    for nodeout, nodein in database.select(CONNTABLE, "nodeout", "nodein"):
        print(nodeout+" "+nodein)
        ret = ret + nodeout+" "+nodein+"\n"
    return ret
        
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
        print("Usage: "+sys.argv[0]+"\n"+
              "listconnections\n"+
              "connect nodeout nodein\n"+
              "disconnect nodeout nodein\n"+
              "remove node")
