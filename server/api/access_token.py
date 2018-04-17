# | Created by Ar4ikov
# | Время: 16.04.2018 - 17:20

from random import choice
from api.database import database
from api.config import config

class access_token():
    __slots__ = ['date', 'script_name', 'ip', 'lenght', '_access_token', 'id']

    db = database(config.getDatabaseName())
    if not db.getTable(config.getAccessTokensTableName()):
        try:
            db.createTable(config.getAccessTokensTableName(),
                           {
                               "type": "INTEGER",
                               "name": "id",
                               "params": "PRIMARY KEY"
                           },
                           {
                               "type": "TEXT",
                               "name": "access_token",
                               "params": ""
                           },
                           {
                               "type": "INTEGER",
                               "name": "lenght",
                               "params": ""
                           },
                           {
                               "type": "TEXT",
                               "name": "script_name",
                               "params": ""
                           },
                           {
                               "type": "INTEGER",
                               "name": "date",
                               "params": ""
                           },
                           {
                               "type": "TEXT",
                               "name": "ip",
                               "params": ""
                           })
        except:
            pass

    def __init__(self, id, date, script_name, _access_token, ip, lenght=64):
        """

        Main class for access token; access token body

        :param id: - id of access token
        :param date: - creating date of access token
        :param script_name: - name of app or script for token had created
        :param _access_token: - access token body
        :param ip: - user remote address
        :param lenght: - lenght of access token
        """
        self.lenght = lenght
        self.date = date
        self.script_name = script_name
        self.ip = ip
        self._access_token = _access_token
        self.id = id

    def getId(self) -> int:
        return self.id

    def getLenght(self) -> int:
        return self.lenght

    def getDate(self) -> int:
        return self.date

    def getScriptName(self) -> str:
        return self.script_name

    def getIp(self) -> str:
        return self.ip

    def getAccessToken(self) -> str:
        return self._access_token

    @staticmethod
    def generateFromMatrix(lenght):
        """

        Generating Matrix for access token

        :param lenght: - lenght of access token
        :return:
        """
        matrix = ["A", "B", "C", "D", "E",
                  "F", "G", "H", "I", "J",
                  "K", "L", "M", "N", "O",
                  "P", "Q", "R", "S", "T",
                  "U", "V", "W", "X", "Y",
                  "Z", "a", "b", "c", "d",
                  "e", "f", "g", "h", "i",
                  "j", "k", "l", "m", "n",
                  "o", "p", "q", "r", "s",
                  "t", "u", "v", "w", "x",
                  "y", "z", "0", "1", "2",
                  "3", "4", "5", "6", "7",
                  "8", "9"]

        Access_token = ""

        for i in range(lenght):
            Access_token = Access_token + choice(matrix)

        return Access_token

    @staticmethod
    def checkValid(token):
        """

        Checking validation of access token

        :param token: - access token
        :return: None if token was not found in database or True if it was found.
        """
        if not access_token.db.getValueFromTable(config.getAccessTokensTableName(), access_token=token):
            return None

        return True

    @staticmethod
    def createAccessToken(ip, script_name, date, lenght=64):
        """

        Creating access token

        :param ip: - user remote address
        :param script_name: - name of app or script for token had created
        :param date: - date of creation
        :param lenght: - lenght of access token
        :return:
        """
        token = access_token.generateFromMatrix(lenght)
        access_token.db.addRow(config.getAccessTokensTableName(), "{last_id}", token, lenght, script_name, date, ip)
        return access_token(id=access_token.db.getLastId(config.getAccessTokensTableName())-1, _access_token=token, lenght=lenght, script_name=script_name, date=date, ip=ip)

    @staticmethod
    def removeAccessToken(id):
        """

        Removing access token from database if it is in database

        :param id:
        :return:
        """
        if not access_token.db.getValueFromTable(config.getAccessTokensTableName(), id=id):
            return None

        access_token.db.removeRow(config.getAccessTokensTableName(), id=id)
        return True

    @staticmethod
    def getAccessTokens() -> list:
        """

        Getting all access tokens

        :return: - List with all tokens class (@access_token)
        """
        tokens = access_token.db.getTable(config.getAccessTokensTableName())
        access_tokens = []
        for token in tokens:
            access_tokens.append(access_token(id=token[0], _access_token=token[1], lenght=token[2], script_name=token[3], date=token[4], ip=token[5]))

        return access_tokens

    @staticmethod
    def getAccessTokenFromDatabase(token=None, id=None):
        """

        Getting access token from database by using `access_token` or `id`

        :param token:
        :param id:
        :return:
        """
        response = None
        if token:
            response = access_token.db.getValueFromTable(config.getAccessTokensTableName(), access_token=token)
        else:
            response = access_token.db.getValueFromTable(config.getAccessTokensTableName(), id=id)

        if not response:
            return None

        return access_token(id=response[0], _access_token=response[1], lenght=response[2], script_name=response[3], date=response[4], ip=response[5])



