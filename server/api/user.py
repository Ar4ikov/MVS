# | Created by Ar4ikov
# | Время: 13.04.2018 - 20:54

from uuid import uuid4 as UUID
from api.database import database
from api.config import config

class user():
    __slots__ = ["vk", "id", "mc", "nickname", "hypixel_key", "banned"]

    db = database(config.getDatabaseName())
    if not db.getTable(config.getAccountsTableName()):
        try:
            db.createTable(config.getAccountsTableName(),
                       {
                           "type": "INTEGER",
                           "name": "Id",
                           "params": "PRIMARY KEY"
                       },
                       {
                           "type": "INTEGER",
                           "name": "vk",
                           "params": ""
                       },
                       {
                           "type": "TEXT",
                           "name": "mc",
                           "params": ""
                       },
                       {
                           "type": "TEXT",
                           "name": "nickname",
                           "params": ""
                       },
                       {
                           "type": "TEXT",
                           "name": "hypixel_key",
                           "params": ""
                       },
                       {
                           "type": "BOOLEAN",
                           "name": "banned",
                           "params": ""
                       })
        except:
            pass

    def __init__(self, vk, id, mc, nickname, hypixel_key, banned):
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

    def getKey(self) -> str:
        return self.hypixel_key

    def isBanned(self) -> bool:
        return self.banned

    @staticmethod
    def getUser(vk=None, id=None, mc=None):
        """

        Getting user from database

        :param vk: - user VK
        :param id: - user id in database
        :param mc: - user MC UUID
        :return: None if user was not found or main user class -> `user` if it was found
        """
        response = None
        if id:
            response = user.db.getValueFromTable(config.getAccountsTableName(), id=id)
        elif vk:
            response = user.db.getValueFromTable(config.getAccountsTableName(), vk=vk)
        else:
            response = user.db.getValueFromTable(config.getAccountsTableName(), mc=mc)

        if not response:
            return None
        else:
            return user(id=response[0], vk=response[1], mc=response[2], nickname=response[3], hypixel_key=response[4], banned=response[5])

    @staticmethod
    def getUsers() -> list:
        """

        Getting all users from database

        :return: List of users which every user is a main class for user -> `user`
        """
        users = user.db.getTable(config.getAccountsTableName())
        players = []
        for player in users:
            players.append(user(id=player[0], vk=player[1], mc=player[2], nickname=player[3], hypixel_key=player[4], banned=player[5]))

        return players

    @staticmethod
    def createUser(vk, mc, nickname, hypixel_key):
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
        user.db.addRow(config.getAccountsTableName(), "{last_id}", vk, mc, nickname, hypixel_key, False)
        return user(id=user.db.getLastId(config.getAccountsTableName())-1, vk=vk, mc=mc, nickname=nickname, hypixel_key=hypixel_key, banned=False)