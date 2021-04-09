import requests
# TODO everything
BASE = "http://127.0.0.1:5000/api/"


response = requests.put(BASE + "users", {"name": "John"})
print(response.json())
input()
response = requests.get(BASE + "user/3")
print(response)

def get_users():

    response = requests.get(BASE + "users")
    print(response.json())


while(True):
    text = input()
    if text == "/users":
        get_users()

