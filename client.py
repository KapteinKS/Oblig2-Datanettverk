import requests
import threading
# TODO still quite a bit
BASE = "http://127.0.0.1:5000/api/"
ID = -1

# Users


def get_users():  # return users
    response = requests.get(BASE + "users", {"id": 1}).json()
    print(response)
    for user in response:
        print(user["name"])

    # TODO format output


def add_user(user_name):  # add user to db
    # TODO type validate string
    #text = input("Please create a username: ")
    response = requests.put(BASE + "users", {"name": '"'+user_name+'"'})
    print(response.json())


def get_user(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + user_id)
        print(response.json())
    else:
        print("Please use a number")


def delete_user(user_id):
    if type(int(user_id)) == int:
        # TODO Make the server give their client their ID upon registration
        response = requests.post(BASE + "user/" + user_id, {"id": 1})
        print(response.json())
    else:
        print("Please enter an ID.")

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
        # print(text)
        # Raw is command only, text[] is command + args
        # TODO Handle index out of bounds
        if raw.startswith("/"):
            if raw == "/help":
                # Print out a help page for all the commands
                pass
            elif raw == "/users":
                get_users()
            elif text[0] == "/register":
                try:
                    add_user(text[1])
                except:
                    print("Please enter a name to register when typing the command")
            elif text[0] == "/user":
                try:
                    get_user(text[1])
                except:
                    print("Please enter a user to get when typing the command")
            elif text[0] == "/delete":
                try:
                    delete_user(text[1])
                except:
                    "Please enter a user to delete when typing the command"


startthread = threading.Thread(target=start)
startthread.start()
