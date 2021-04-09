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
    # TODO type validate string
    text = input("Please create a username: ")
    response = requests.put(BASE + "users", {"name": '"'+text+'"'})
    print(response.json())


def get_user(user_id):
    if type(user_id) == "int":
        response = requests.get(BASE + "user/" + user_id)
        print(response.json())
    else:
        print("Please use a number")


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
        raw = input()
        text = raw.split(" ")

        # Raw is command only, text[] is for command + args
        if raw == "/users":
            get_users()
        elif raw == "/register":
            add_user()
        elif text[0] == "/user":
            get_user(text[1])


startthread = threading.Thread(target=start)
startthread.start()
