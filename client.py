import requests
import threading
# TODO everything
BASE = "http://127.0.0.1:5000/api/"


# Users

def get_users():  # return users
    response = requests.get(BASE + "users")
    print(response.json())
    # TODO format output


def add_user():  # add user to db
    response = requests.put(BASE + "users", {"name": "John"})
    print(response.json())


def get_user(user_id):
    pass


def delete_user(user_id):
    pass

# Rooms


def get_rooms():
    pass


def add_room():
    pass


def get_room(room_id):
    pass

# RoomUsers


def get_room_users():
    pass


def add_room_user(room_id):
    pass

# Messages


def get_messages(room_id):
    pass


def get_user_messages(room_id, user_id):
    pass


def post_message(room_id, user_id):
    pass

# Start


def start():
    while(True):
        text = input()

        if text == "/users":
            get_users()
        elif text == "/register":
            add_user()


startthread = threading.Thread(target=start)
startthread.start()
