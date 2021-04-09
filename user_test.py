import requests
BASE = "http://127.0.0.1:5000/api/"
# response = requests.get(BASE + "users")
# print(response.json())
# input()
# 
response = requests.post(BASE + "user/1", {"id": 2})
print(response)
