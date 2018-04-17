# | Created by Ar4ikov
# | Время: 17.04.2018 - 00:14

# Импорт модуля
import mvs_client as MVS

# Объявление экземпляра класса MVS_Client
mvs = MVS.MVS_Client(
    server="http://127.0.0.1",
    access_token="D7MSoV0qiRn5WzSBDdJicrGpLCxznaD1g0sFuGvATnu2SdRx108M5otnsiVBZAVY"
)

# Получаем пользователя с MVS Id 1
response = mvs.getUser(id=1).getResponse()
print(response)

# Получаем ошибку (1. Unknown Method)
response = mvs.getUUseeeer().getErrorCode()
print(response)