import requests
BASE = "http://127.0.0.1:5000/api/"
response = requests.get(BASE + "users")
print(response.json())
input()

response = requests.get(BASE + "user/1")
print(response.json())
# 
# response = requests.post(BASE + "user/1", {"id": 2})
# print(response)
input()
requests.put(BASE + "rooms", {"name": "sexting"})
response = requests.put(BASE + "room/2/users", {"id": 1})
print(response.json())
