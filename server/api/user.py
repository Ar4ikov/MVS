# | Created by Ar4ikov
# | Время: 13.04.2018 - 20:54

from uuid import uuid4 as UUID
from api.database import database
from api.config import config
import requests

class user():
    __slots__ = ["vk", "id", "mc", "nickname", "confirmation_type", "hypixel_key", "banned"]

    db = database(config.getDatabaseName())
    db.getCursor().execute("CREATE TABLE IF NOT EXISTS accounts "
                           "(id INTEGER PRIMARY KEY, "
                           "vk INTEGER  NOT NULL, "
                           "mc TEXT  NOT NULL, "
                           "nickname TEXT  NOT NULL, "
                           "confirmation_type TEXT NOT NULL, "
                           "hypixel_key TEXT  NOT NULL, "
                           "banned BOOLEAN  NOT NULL"
                           ")")
    db.getConnection().commit()

    def __init__(self, vk, id, mc, nickname, confirmation_type, hypixel_key, banned):
        """

        Main user class; user body

        :param vk: user VK
        :param id: user id in database
        :param mc: user MC UUID
        :param nickname: user nickname
        :param hypixel_key: user Hypixel API Key
        :param banned: boolean, if True, user has already banned in MVS, if False - has not banned yet.
        """
        self.vk = vk
        self.id = id
        self.mc = mc
        self.nickname = nickname
        self.confirmation_type = confirmation_type
        self.hypixel_key = hypixel_key
        self.banned = banned

    def getVK(self) -> UUID:
        return self.vk

    def getId(self) -> int:
        return self.id

    def getMC(self) -> str:
        return self.mc

    def getNickName(self) -> str:
        return self.nickname

    def getConfirmationType(self) -> str:
        return self.confirmation_type

    def getKey(self) -> str:
        return self.hypixel_key

    def isBanned(self) -> bool:
        return self.banned

    @staticmethod
    def getResponse(id=None, vk=None, mc=None, nickname=None):
        response = None
        if id:
            response = user.db.getValueFromTable(config.getAccountsTableName(), id=id)
        elif vk:
            response = user.db.getValueFromTable(config.getAccountsTableName(), vk=vk)
        elif nickname:
            response = user.db.getValueFromTable(config.getAccountsTableName(), nickname=nickname)
        else:
            response = user.db.getValueFromTable(config.getAccountsTableName(), mc=mc)

        print(response)
        return response

    @staticmethod
    def getUser(vk=None, id=None, mc=None, nickname=None):
        """

        Getting user from database

        :param vk: - user VK
        :param id: - user id in database
        :param mc: - user MC UUID
        :return: None if user was not found or main user class -> `user` if it was found
        """
        print(vk, id, mc, nickname)
        response = user.getResponse(id, vk, mc, nickname)

        if not response:
            return None
        else:
            return user(id=response[0], vk=response[1], mc=response[2], nickname=response[3], confirmation_type=response[4], hypixel_key=response[5], banned=response[6])

    @staticmethod
    def getUsers() -> list:
        """

        Getting all users from database

        :return: List of users which every user is a main class for user -> `user`
        """
        users = user.db.getTable(config.getAccountsTableName())
        players = []
        for player in users:
            players.append(user(id=player[0], vk=player[1], mc=player[2], nickname=player[3], confirmation_type=player[4], hypixel_key=player[5], banned=player[6]))

        return players

    @staticmethod
    def updateNickname(id=None, vk=None, mc=None, nickname=None):
        response = user.getResponse(id, vk, mc, nickname)

        if not response:
            return None

        names = [eval(x) for x in requests.get("https://api.mojang.com/user/profiles/{}/names".format(response[2])).text.replace("[", "").replace("]", "").split(", ")]

        new_names = []
        if type(names[0]) == tuple:
            for name in names[0]:
                new_names.append(name)

        print(new_names)
        if type(names[0]) == tuple:
            names = new_names
        new_nickname = names[-1]
        user.db.getCursor().execute("UPDATE `{}` SET nickname='{}' WHERE mc='{}'".format(config.getAccountsTableName(), new_nickname["name"], response[2]))
        user.db.getConnection().commit()

        return {"new_nickname": new_nickname}

    @staticmethod
    def createUser(vk, mc, nickname, hypixel_key, confirmation_type):
        """

        Creating user

        :param vk: - user VK
        :param mc: - user MC UUID
        :param nickname: user nickname
        :param hypixel_key: - Hypixel API Key
        :return: - class user
        """

        if user.db.getValueFromTable(config.getAccountsTableName(), vk=vk) or user.db.getValueFromTable(config.getAccountsTableName(), mc=mc):
            return None
        user.db.getCursor().execute("""INSERT INTO `{}` (vk, mc, nickname, confirmation_type, hypixel_key, banned) 
                                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""".format(
            config.getAccountsTableName(), vk, mc, nickname, confirmation_type, hypixel_key, False
        ))
        user.db.getConnection().commit()

        return user(id=user.db.getLastId(config.getAccountsTableName())-1, vk=vk, mc=mc, nickname=nickname, confirmation_type=confirmation_type, hypixel_key=hypixel_key, banned=False)

    @staticmethod
    def banUser(id, vk, mc, nickname):
        """

        Ban user in MVS

        :param id: user Id in MVS
        :param vk: user VK
        :param mc: user MC UUID
        :param nickname: user MC Nickname
        :return: boolean True or None
        """

        response = user.getResponse(id, vk, mc, nickname)

        if not response:
            return None

        if response[6] == "True":
            return False

        user.db.getCursor().execute("""UPDATE `{}` SET banned='{}' WHERE mc='{}'""".format(
            config.getAccountsTableName(), True, response[2]
        ))
        user.db.getConnection().commit()

        return True

    @staticmethod
    def unbanUser(id, vk, mc, nickname):
        """

        Unban user in MVS

        :param id: user Id in MVS
        :param vk: user VK
        :param mc: user MC UUID
        :param nickname: user MC Nickname
        :return: boolean True or None
        """

        response = user.getResponse(id, vk, mc, nickname)

        if not response:
            return None

        if response[6] == "False":
            return False

        user.db.getCursor().execute("""UPDATE `{}` SET banned='{}' WHERE mc='{}'""".format(
            config.getAccountsTableName(), False, response[2]
        ))
        user.db.getConnection().commit()

        return True