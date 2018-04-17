# | Created by Ar4ikov
# | Время: 14.04.2018 - 14:15
from server.api.errors import error
from flask import jsonify

class json_scheme():
    @staticmethod
    def createResponse(**kwargs) -> str:
        return jsonify({"status": "success", "response": kwargs})

    @staticmethod
    def createError(error: error) -> str:
        return jsonify({"status": "failed", "code": error.getCode(), "cause": error.getCause()})