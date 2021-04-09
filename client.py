import requests
import threading
# TODO everything
BASE = "http://127.0.0.1:5000/api/"


#response = requests.get(BASE + "user/3")
# print(response.json())


def get_users():
    response = requests.get(BASE + "users")
    print(response.json())


def put_user():
    response = requests.put(BASE + "users", {"name": "John"})
    print(response.json())


def start():
    while(True):
        text = input()
        if text == "/users":
            get_users()
        if text == "/register":
            put_user()


thread = threading.Thread(target=start)
thread.start()
