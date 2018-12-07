'''
    Database.py part of TheFlow
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

import mysql.connector

class Database:
    def __init__(self, host, user, passwd, database):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
    
    def select(self, table, *args, **kwargs):
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        query = "SELECT "
        if len(args) == 0:
            query = query + "* "
        else:
            query = query + ", ".join(args) + " "
        query = query + "FROM "+table
        if len(kwargs.keys()) > 0:
            query = query + " WHERE "
            where = []
            for col in kwargs:
                where.append(col + "='" + str(kwargs[col]) + "'")
            query = query + " AND ".join(where)
        cursor.execute(query)
        ret = []
        for row in cursor.fetchall():
            if len(row)==1:
                ret.append(row[0])
            else:
                ret.append(tuple(row))
        return ret
        
    def insert(self, table, **kwargs):
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        query="INSERT INTO "+table+" ("
        cols=[]
        values=[]
        for col in kwargs:
            cols.append(col)
            values.append("'"+str(kwargs[col])+"'")
        query = query+ ", ".join(cols) +") VALUES ("+ ", ".join(values)+ ")"
        cursor.execute(query)
        database.commit()
        
    def update(self, table, **kwargs):
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        query = "UPDATE "+table+" SET "
        for col in kwargs:
            if col == "where":
                query = query + "WHERE "
            else:
                query = query + col + " = '" + str(kwargs[col]) + "' "
        cursor.execute(query)
        database.commit()
        
    def delete(self, table, **kwargs):
        database = mysql.connector.connect(host=self.host, user=self.user, passwd=self.passwd, database=self.database)
        cursor = database.cursor()
        query = "DELETE FROM "+table+" WHERE "
        where = []
        for col in kwargs:
            where.append(col + " = '" + kwargs[col] + "'")
        query = query + " AND ".join(where)
        cursor.execute(query)
        database.commit()
