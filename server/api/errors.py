# | Created by Ar4ikov
# | Время: 14.04.2018 - 14:08

class error():
    __slots__ = ['code', 'cause']

    def __init__(self, code, cause):
        self.code = code
        self.cause = cause

    def getCode(self):
        return self.code

    def getCause(self):
        return self.cause

class errors(Exception):
    @staticmethod
    def UNKNOWN_METHOD(method):
        return error(1, "Unknown Method `" + method + "`")

    @staticmethod
    def MISSED_PARAMS():
        return error(2, "One of params is missing")

    @staticmethod
    def INCORRECT_KEY():
        return error(3, "This API Key is incorrect or invalid or expended a long moments ago")

    @staticmethod
    def USER_NOT_FOUND():
        return error(4, "That user cannot be found.")

    @staticmethod
    def PERMISSIONS_DENY():
        return error(5, "You do not have permissions to call this method. Contact with administrator of the system to get permissions.")

    @staticmethod
    def USER_ALREADY_EXIST():
        return error(6, "That user is already exist in Minecraft Verification System Database")

    @staticmethod
    def INVALID_ACCESS_TOKEN():
        return error(7, "That Access Token is invalid or have not created yet")

    @staticmethod
    def VERIFY_IDENTITY():
        return error(8, "Please, verify your identity to continue (send valid `access_token` or `hypixel_key`)")

    @staticmethod
    def ALREADY_BANNED():
        return error(9, "This user has already banned.")

    @staticmethod
    def NOT_BANNED_YET():
        return error(10, "This user hasn't banned yet.")