import requests
BASE = "http://127.0.0.1:5000/api/"
response = requests.get(BASE + "users", {"id": 5})
print(response.json())
# input()

# response = requests.get(BASE + "user/1")
# print(response.json())
# 
# response = requests.post(BASE + "user/1", {"id": 2})
# print(response)
# input()
# requests.put(BASE + "rooms", {"name": "sexting"})
# input()
# response = requests.put(BASE + "room/2/users", {"id": 1})
# print(response.json())

# response = requests.post(BASE + "room/1/1/messages", {"id": 1, "message": "This is a test message from user_test.py"})
# print(response.json())
