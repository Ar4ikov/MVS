# | Created by Ar4ikov
# | Время: 14.04.2018 - 14:59

import requests

class hypixe_request():
    def __init__(self, status, *args):
        data = [x for x in args]
        data[0].pop("success")

        self.status = status
        self.response = data[0]

    def getStatus(self) -> bool:
        return self.status

    def getResponse(self) -> dict:
        return self.response

class hypixel_api():
    """

    I do not say anymore about this. Simple Hypixel API Client Wrapper, no more.

    """
    def __init__(self, server, api_key):
        self.server = server
        self.api_key = api_key

    def getServer(self):
        return self.server

    def getApiKey(self):
        return self.api_key

    def request(self, method, **data) -> hypixe_request:
        data['key'] = self.getApiKey() or "Not_stayed"

        response_body = requests.get(self.getServer() + "/" + method, params=data)
        response = eval(response_body.text.replace("false", "False").replace("true", "True").replace("null", "None"))

        return hypixe_request(response['success'], response)