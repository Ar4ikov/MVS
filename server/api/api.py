# | Created by Ar4ikov
# | Время: 13.04.2018 - 20:36

import flask, hashlib, requests
from time import time
from flask import request, render_template, session
from api.user import user
from api.errors import errors
from api.scheme import json_scheme
from api.hypixel_api import hypixel_api
from api.access_token import access_token
from api.config import config
from api.custom_database import custom_database

__version__ = "1.1.0"

class api():
    def __init__(self, app: flask.Flask, host="localhost", port=80):
        self.app = app
        self.host = host
        self.port = port

    def getApp(self):
        return self.app

    def routing(self) -> None:
        """

        Describe there your event listeners for routing methods from server

        :param app: - flask.Flask
        :return: - None
        """
        app = self.getApp()
        app.config['SECRET_KEY'] = config.getSessionCode()

        @app.route("/", methods=['GET'])
        def welcome():
            """

            Main Page

            :return:
            """
            if not user.db.getTable(config.getAdminsTableName()):
                return render_template("/index.html")
            else:
                return render_template("/main_page.html")

        @app.route("/confirmSetup", methods=['GET', 'POST'])
        def confirmSetup():
            """

            Setup Page

            :return:
            """
            if not user.db.getTable(config.getAdminsTableName()):
                data = request.form

                username = data.get('username')
                password = hashlib.sha256(data.get('password').encode('utf-8')).hexdigest()
                first_name = data.get('first_name')
                password_repeat = hashlib.sha256(data.get('password-repeat').encode('utf-8')).hexdigest()

                if password != password_repeat:
                    return '<meta http-equiv="refresh" content="0; url=/#passwords-is-not-matches" />'

                user.db.getCursor().execute("""CREATE TABLE IF NOT EXISTS admin 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            username TEXT  NOT NULL, 
                            password TEXT  NOT NULL, 
                            first_name TEXT  NOT NULL
                            )""")
                user.db.getConnection().commit()

                user.db.getCursor().execute("""INSERT INTO `{}` (username, password, first_name)
                                  VALUES ('{}', '{}', '{}')""".format(
                    config.getAdminsTableName(), username, password, first_name
                ))
                user.db.getConnection().commit()

                return '<meta http-equiv="refresh" content="0; url=/" />'
            else:
                return json_scheme.createError(errors.UNKNOWN_METHOD(request.path[1:])), 404

        @app.route("/updateNickname", methods=["GET", "POST"])
        def updateNicknameCommand():
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) == 0:
                return json_scheme.createError(errors.MISSED_PARAMS())

            atv = access_token.checkValid(data.get("access_token"))
            if not atv and not data.get('hypixel_key'):
                return json_scheme.createError(errors.VERIFY_IDENTITY())

            player = user.getUser(id=data.get("id"), vk=data.get("vk"), mc=data.get("mc"), nickname=data.get("nickname"))
            if not player:
                return json_scheme.createError(errors.USER_NOT_FOUND())

            if not atv and player.getKey() != data.get("hypixel_key"):
                return json_scheme.createError(errors.INCORRECT_KEY())

            response = user.updateNickname(data.get("id"), data.get("vk"), data.get("mc"), data.get("nickname"))

            return json_scheme.createResponse(new_nickname=response["new_nickname"])

        @app.route("/createUser", methods=['GET', 'POST'])
        def createUserCommand():
            """

            Creating user
            Private method. Needs an `access_token`, which you can manage in your admin-panel

            :return:
            """
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) < 2 or not data.get("vk"):
                return json_scheme.createError(errors.MISSED_PARAMS())

            response = self.createUser(data.get('vk'), data.get('hypixel_key'))
            if response == None:
                return json_scheme.createError(errors.INCORRECT_KEY())

            if response == False:
                return json_scheme.createError(errors.USER_ALREADY_EXIST())

            return json_scheme.createResponse(user=response)

        @app.route("/getUsers", methods=['GET', 'POST'])
        def getUsersCommand():
            return json_scheme.createResponse(users=self.getUsers())

        @app.route("/banUser", methods=["GET", "POST"])
        def banUserCommand():
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) < 2 and data.get("access_token"):
                return json_scheme.createError(errors.MISSED_PARAMS())

            if not access_token.checkValid(data.get("access_token")):
                return json_scheme.createError(errors.INVALID_ACCESS_TOKEN())

            response = user.banUser(data.get('id'), data.get('vk'), data.get('mc'), data.get("nickname"))
            if response is None:
                return json_scheme.createError(errors.USER_NOT_FOUND())

            if not response:
                return json_scheme.createError(errors.ALREADY_BANNED())

            return json_scheme.createResponse()

        @app.route("/unbanUser", methods=["GET", "POST"])
        def unbanUserCommand():
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) < 2 and data.get("access_token"):
                return json_scheme.createError(errors.MISSED_PARAMS())

            if not access_token.checkValid(data.get("access_token")):
                return json_scheme.createError(errors.INVALID_ACCESS_TOKEN())

            response = user.unbanUser(data.get('id'), data.get('vk'), data.get('mc'), data.get("nickname"))
            if response is None:
                return json_scheme.createError(errors.USER_NOT_FOUND())

            if not response:
                return json_scheme.createError(errors.NOT_BANNED_YET())

            return json_scheme.createResponse()

        @app.route("/getUser", methods=['GET', 'POST'])
        def getUserCommand():
            """

            Getting user from MVS Database

            :return:
            """
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) == 0:
                return json_scheme.createError(errors.MISSED_PARAMS())

            user = self.getUser(data.get('id'), data.get('vk'), data.get('mc'), data.get("nickname"))
            if not user:
                return json_scheme.createError(errors.USER_NOT_FOUND())

            return json_scheme.createResponse(user=user)

        @app.route("/confirmUser", methods=['GET', 'POST'])
        def confirmUserCommand():
            """

            Checking validation of `hypixel_key`

            :return:
            """
            if request.method == "GET":
                data = request.args
            else:
                data = request.form

            if len([x for x in data.keys()]) == 0:
                return json_scheme.createError(errors.MISSED_PARAMS())

            return json_scheme.createResponse(key_info=str(self.confirmUser(data.get('hypixel_key'))))

        @app.route('/admin', methods=['GET', 'POST'])
        def admin():
            """

            Administrator Panel

            :return:
            """
            if not user.db.getTable(config.getAdminsTableName()):
                return '<meta http-equiv="refresh" content="0; url=/" />'

            data = request.form

            if session.get("logged") and data.get("type") == "create_new":
                script_name = data.get("script_name")
                current_time = int(str(int(time()))[0:10])
                current_ip = request.remote_addr

                access_token.createAccessToken(current_ip, script_name, current_time)
                return '<meta http-equiv="refresh" content="0; url=/admin" />'

            if session.get("logged") and data.get("type") == "delete_token":
                id = data.get("id")
                access_token.removeAccessToken(id)

                return '<meta http-equiv="refresh" content="0; url=/admin" />'

            if session.get("logged"):
                return render_template("/admin.html",
                                        access_tokens=self.generateAccessTokenTable())

            if not session.get("logged") and data.get("type") != "auth":
                return render_template("/login.html", recaptcha_secret=config.getReCaptchaPublic())

            if data.get("type") == "auth":
                captcha = eval(requests.post("https://www.google.com/recaptcha/api/siteverify", params={
                    "secret": config.getReCaptchaSecret(),
                    "response": data.get("g-recaptcha-response"),
                    "remoteip": request.remote_addr
                }).text.replace("true", "True").replace("false", "False").replace("null", "None"))

                if not captcha.get("success"):
                    return '<meta http-equiv="refresh" content="0; url=/admin#captcha-error" />'

                username = data.get("username")
                password = hashlib.sha256(data.get("password").encode("utf-8")).hexdigest()

                row = user.db.getValueFromTable(config.getAdminsTableName(), username=username)
                if not row:
                    return '<meta http-equiv="refresh" content="0; url=/admin#user-not-found" />'

                if row[2] != password:
                    return '<meta http-equiv="refresh" content="0; url=/admin#incorrect-password" />'

                session["logged"] = True
                return render_template("/admin.html", access_tokens=self.generateAccessTokenTable())


        @app.route('/logout', methods=['GET'])
        def logout():
            """

            Logout

            :return:
            """
            if session.get('logged'): session.pop('logged')
            return '<meta http-equiv="refresh" content="0; url=/admin" />'

        @app.errorhandler(404)
        def unk_method(e):
            """

            Custom handling 404 error

            :param e: - Error
            :return:
            """
            return json_scheme.createError(errors.UNKNOWN_METHOD(request.path[1:])), 404

        # Starting Server there
        app.run(host=self.host, port=self.port)

    # Methods -------------------->

    def getUsers(self):
        """

        Getting all users from database

        :return:
        """

        users = []
        usercls = user.getUsers()
        for player in usercls:
            users.append({
                "id": player.getId(),
                "vk": player.getVK(),
                "mc": player.getMC(),
                "nickname": player.getNickName(),
                "confirmation_type": player.getConfirmationType(),
                "is_banned": player.isBanned()
            })

        return users

    def getUser(self, id, vk, mc, nickname):
        """

        Getting a user from database by `id` or `vk` or `mc`

        :param id: Id in database
        :param vk: VK Id
        :param mc: Minecraft UUID
        :return: JSON with user info
        """

        usercls =  user.getUser(id=id, vk=vk, mc=mc, nickname=nickname)
        if not usercls:
            return None

        return {
            "id": usercls.getId(),
            "vk": usercls.getVK(),
            "mc": usercls.getMC(),
            "nickname": usercls.getNickName(),
            "confirmation_type": usercls.getConfirmationType(),
            "is_banned": usercls.isBanned()
        }

    def createUser(self, vk, hypixel_key):
        """

        Creating an unique user by sending `VK` and `hypixel_key` (Hypixel API Key)

        :param vk: - VK Id
        :param hypixel_key: - Hypixel API Key
        :return: JSON with user or False if user is already exist or None if `hypixel_key` is invalid
        """

        response = self.confirmUser(hypixel_key)
        if response:
            uuid = response.get('ownerUuid')
            nickname = response.get('nickname')
            confirmation_type = response.get("confirmation_type")

            usercls = user.createUser(vk=vk, mc=uuid, nickname=nickname, confirmation_type=confirmation_type, hypixel_key=hypixel_key)
            if not usercls:
                return False

            return {
                "id": usercls.getId(),
                "vk": usercls.getVK(),
                "mc": usercls.getMC(),
                "nickname": usercls.getNickName(),
                "confirmation_type": usercls.getConfirmationType(),
                "is_banned": usercls.isBanned()
            }
        else:
            return None

    def confirmUser(self, hypixel_key):
        """

        Checking the validation of `hypixel_key`

        :param hypixel_key: - Hypixel API Key
        :return: JSON with `hypixel_key` and `ownerUuid` for `mc`
        """
        if config.getEABool():
            mysql = custom_database()

            request = mysql.getRow(access_token=hypixel_key)
            if not request:
                hypixel = hypixel_api("https://api.hypixel.net", hypixel_key)
                response = hypixel.request("key")
                if not response.getStatus():
                    return False
                else:
                    nickname = hypixel.request("player", uuid=response.getResponse().get("record").get('ownerUuid')).getResponse()[
                        "player"].get("displayname")
                    return {'confirmation_type': 'hypixel_key', 'nickname': nickname, 'hypixel_key': hypixel_key,
                            'ownerUuid': response.getResponse().get("record").get('ownerUuid')}
            else:
                return {'confirmation_type': 'mvs_auth', 'nickname': request[4], 'hypixel_key': request[2],
                        'ownerUuid': request[1]}

        hypixel = hypixel_api("https://api.hypixel.net", hypixel_key)
        response = hypixel.request("key")
        if not response.getStatus():
            return False
        else:
            nickname = hypixel.request("player", uuid=response.getResponse().get("record").get('ownerUuid')).getResponse()["player"].get("displayname")
            return {'confirmation_type': 'hypixel_key', 'nickname': nickname,'hypixel_key': hypixel_key, 'ownerUuid': response.getResponse().get("record").get('ownerUuid')}

    def generateAccessTokenTable(self):
        """

        Generating HTML-Table with Access Tokens

        :return:
        """
        access_tokens = ""
        i = 0
        for row in access_token.getAccessTokens():
            if i % 2 == 0:
                access_tokens = access_tokens + "<tr class='light-row'>\n" \
                                                  "    <td>{}</td>\n" \
                                                  "    <td>{}</td>\n" \
                                                  "    <td>{}</td>\n" \
                                                  "    <td>{}</td>\n" \
                                                  "    <td>{}</td>\n" \
                                                  "<tr>\n".format(row.getAccessToken(), row.getDate(), row.getScriptName(), row.getIp(), '<button id="{}" onclick="javascript:removeItem(this)" class="remove">x</button>'.format(row.getId()))
            else:
                access_tokens = access_tokens + "<tr class='dark-row'>\n" \
                                                        "    <td>{}</td>\n" \
                                                        "    <td>{}</td>\n" \
                                                        "    <td>{}</td>\n" \
                                                        "    <td>{}</td>\n" \
                                                        "    <td>{}</td>\n" \
                                                        "<tr>\n".format(row.getAccessToken(), row.getDate(), row.getScriptName(), row.getIp(), '<button id="{}" onclick="javascript:removeItem(this)" class="remove">x</button>'.format(row.getId()))
            i += 1

        return access_tokens