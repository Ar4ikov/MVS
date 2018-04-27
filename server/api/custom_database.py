# | Created by Ar4ikov
# | Время: 26.04.2018 - 12:16

import mysql.connector as mysql
from api.config import config

class custom_database:
    def __init__(self,
                 host=config.getEAHost(),
                 port=config.getEAPort(),
                 user=config.getEALogin(),
                 password=config.getEAPassword(),
                 name=config.getEADatabase()):
        self.sql = mysql.connect(host=host, port=port, user=user, password=password, database=name)

    def getSql(self) -> mysql.connect:
        return self.sql

    def getCursor(self):
        return self.sql.cursor()

    def getTable(self):
        self.getCursor().execute("SELECT * FROM `{}`".format(config.getEATable()))
        return self.getCursor().fetchall()

    def getRow(self, **values):
        for key, value in values.items():
            query = "SELECT * FROM `{}` WHERE `{}`='{}' LIMIT 0, 1".format(
                config.getEATable(),
                key,
                value
            )

            cursor = self.getCursor()
            cursor.execute(query)
            response = cursor.fetchone()

            if not response:
                return None
            else:
                return response