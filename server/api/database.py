# | Created by Ar4ikov
# | Время: 13.04.2018 - 23:10

import sqlite3
import re
import time

class database():
    def __init__(self, dbname=':memory:'):
        self.db = sqlite3.connect(dbname)
        self.cursor = self.db.cursor()
        self.placeholders = {
            "{last_id}": self.getLastId,
            "{time_now}": self.getTime
        }

    def getCursor(self):
        return self.db.cursor()

    def getConnection(self):
        return self.db

    def getTime(self):
        return str(time.time())[0:10]

    def getLastId(self, table=None):
        try:
            self.cursor.execute("SELECT * FROM {table}".format(table=table))
        except:
            return False
        result = self.cursor.fetchall()
        if len(result) == 0:
            return 1
        return result[-1][0]+1

    def createTable(self, table, *rows):
        strings = ""
        i = 0
        for string in rows:
            i += 1
            table_name = str(string['name'])
            table_type = str(string['type'])
            table_type = re.sub('int', 'INTEGER', table_type)
            table_params = str(string['params']).upper()
            if len(rows) == i:
                strings = strings + table_name + " " + table_type + " " + table_params + " NOT NULL"
            else:
                strings = strings + table_name + " " + table_type + " " + table_params + " NOT NULL" + ", "
        request = "CREATE TABLE {table} ({inputs})".format(table=table, inputs=strings)
        self.cursor.execute(request)
        self.db.commit()
        return self.cursor.fetchall()

    def addRow(self, table, *args):
        strings = ""
        i = 0
        for string in args:
            if str(string)[0] == '{' and str(string)[-1] == '}':
                string = self.placeholders[str(string)](table=table)
            i += 1
            value = str(string)
            if len(args) == i:
                strings = strings + "'" + value + "'"
            else:
                strings = strings + "'" + value + "'" + ", "
        request = 'INSERT INTO {table} VALUES ({inputs})'.format(table=table, inputs=strings)
        #print(request)
        self.cursor.execute(request)
        self.db.commit()

    def removeRow(self, table, **column):
        for row in column.items():
            col = row[0]
            value = row[1]
        self.cursor.execute("DELETE FROM {table} WHERE ({column}='{value}')".format(table=table, column=col, value=value))
        self.db.commit()

    def getTable(self, table):
        try:
            self.cursor.execute('SELECT * FROM {}'.format(table))
            result = self.cursor.fetchall()
            return result
        except:
            return None

    def getValueFromTable(self, table, **kwargs):
        for item in kwargs.items():
            key = item[0]
            value = item[1]
            self.cursor.execute("SELECT * FROM {table} WHERE {key}='{value}'".format(table=table, value=value, key=key))
            result = self.cursor.fetchone()
            return result