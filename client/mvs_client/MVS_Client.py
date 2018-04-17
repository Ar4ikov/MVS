# | Created by Ar4ikov
# | Время: 17.04.2018 - 00:01

import requests

__version__ = "1.0.0"

class MVS_Response():
    def __init__(self, status, response=None, error_code=None, cause=None, response_body=None):
        self.status = status
        self.response = response
        self.error_code = error_code
        self.cause = cause
        self.response_body = response_body

    def getStatus(self) -> str:
        return self.status

    def getResponse(self) -> dict:
        return self.response

    def getErrorCode(self) -> int:
        return self.error_code

    def getCause(self) -> str:
        return self.cause

    def getResponseBody(self) -> dict:
        return self.response_body

class MVS_Client_Obj():
    def __init__(self, server, method, access_token):
        self.server = server
        self.method = method
        self.access_token = access_token

    def __call__(self, **data) -> MVS_Response:
        return self.getRequest(**data)

    def getRequest(self, **data) -> MVS_Response:
        data["access_token"] = self.access_token
        response_body = requests.post(self.server + "/" + self.method, data=data)
        response = eval(response_body.text)

        return MVS_Response(response.get("status"), response_body=response, response=response.get("response"), error_code=response.get("code"), cause=response.get("cause"))

class MVS_Client():
    def __init__(self, server, access_token):
        self.access_token = access_token
        self.server = server

    def __getattr__(self, method) -> MVS_Client_Obj:
        return MVS_Client_Obj(self.server, method, self.access_token)
