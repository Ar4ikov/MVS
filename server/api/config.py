# | Created by Ar4ikov
# | Время: 16.04.2018 - 21:03

from configparser import ConfigParser

class config():
    config_path = "config.ini"
    cfg = ConfigParser()
    cfg.read(config_path, "utf-8")

    @staticmethod
    def getDatabaseName():
        return config.cfg.get("DATABASE", "database_name")

    @staticmethod
    def getAccountsTableName():
        return config.cfg.get("TABLES", "accounts")

    @staticmethod
    def getAdminsTableName():
        return config.cfg.get("TABLES", "admins")

    @staticmethod
    def getAccessTokensTableName():
        return config.cfg.get("TABLES", "access_tokens")

    @staticmethod
    def getHost():
        return config.cfg.get("SERVER", "host")

    @staticmethod
    def getPort():
        return int(config.cfg.get("SERVER", "port"))

    @staticmethod
    def getSessionCode():
        return config.cfg.get("FLASK", "session_code")

    @staticmethod
    def getReCaptchaSecret():
        return config.cfg.get("RECAPTCHA", "recaptcha_secret")

    @staticmethod
    def getReCaptchaPublic():
        return config.cfg.get("RECAPTCHA", "recaptcha_public")

    # External Auth
    # --------------------

    @staticmethod
    def getEABool() -> bool:
        if config.cfg.get("Auth", "external_authorization") == "True":
            return True
        else:
            return False

    @staticmethod
    def getEAHost():
        return config.cfg.get("Auth", "ea_host")

    @staticmethod
    def getEAPort():
        return config.cfg.get("Auth", "ea_port")

    @staticmethod
    def getEALogin():
        return config.cfg.get("Auth", "ea_login")

    @staticmethod
    def getEAPassword():
        return config.cfg.get("Auth", "ea_password")

    @staticmethod
    def getEADatabase():
        return config.cfg.get("Auth", "ea_database")

    @staticmethod
    def getEATable():
        return config.cfg.get("Auth", "ea_table")
