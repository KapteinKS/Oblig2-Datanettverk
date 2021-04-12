import requests
import threading
# TODO just a little bit less now
BASE = "http://127.0.0.1:5000/api/"
ID = -1

HELP_CONNECTED = """/users gives a list of users
/user <id> gives the user"""
HELP_NOT_CONNECTED = """When not connected you can only use the /help, /register or /connect
commands. Please register as a new user then connect with your given ID.
Use /register <name> and then /connect <ID>."""
# USERS #######################################################################


def connect(user_id):
    global ID
    ID = user_id


def get_users():  # return users
    response = requests.get(BASE + "users", {"id": 1}).json()
    for user in response:
        print(user["name"])

    # TODO format output


def add_user(user_name):  # add user to db
    # TODO type validate string
    # text = input("Please create a username: ")
    response = requests.put(BASE + "users", {"name": user_name})
    print(response.json())


def get_user(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + user_id, {"id": ID})
        print(response.json())
    else:
        print("Please use a number")


def delete_user(user_id):
    if type(int(user_id)) == int:
        response = requests.post(BASE + "user/" + str(user_id), {"id": ID})
        print(response.json())
        if response.json() == "User deleted":
            list_of_globals = globals()
            list_of_globals['ID'] = -1
            print("You have now been logged out after deleting your user")
    else:
        print("Please enter an ID.")

# ROOMS #######################################################################
def get_rooms():
    response = requests.get(BASE + "rooms", {"id": ID})
    for room in response:
        print(room)
        # TODO: Formatting output

def add_room(room_name):
    response = requests.put(BASE + "rooms", {"id" : ID, "name": room_name})
    print(response.json())
    # TODO: Format output


def get_room(room_id):
    if type(int(room_id)) == int:
        response = requests.get(BASE + "room/" + room_id, {"id": ID})
        print(response.json())
        # TODO: Formatting output
    else:
        print("Please use a number")

# ROOM USERS ##################################################################

def get_room_users(room_id):
    if type(int(room_id)) == int:
        #"/api/room/<int:room_id>/users"
        response = requests.get(BASE + "room/" + str(room_id) + "/users", {"id": ID})
        print(response.json())
        # TODO: Formatting output
    else:
        print("Please use a number")


# TODO: this
def add_room_user(room_id):
    pass

# MESSAGES ####################################################################


# TODO: Format response
def get_messages(room_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/messages", {"id": ID})
        for message in response:
            print(message)


# TODO: this
def get_user_messages(room_id, user_id):
    pass


# TODO: this
def post_message(room_id, user_id, message):
    pass


# TODO: this
def receive_thread():
    # TODO: Receiving messages and prompts from server.
    pass

# STARTUP #####################################################################


def send_thread():
    while True:
        raw = input(":")
        text = raw.split(" ")
        # Raw is command only, text[] is command + args
        if raw.startswith("/"):
            if ID >= 0:
                if raw == "/help":
                    # Print out a help page for all the commands
                    print(HELP_CONNECTED)
                    pass
                elif raw == "/users":
                    get_users()

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
                elif raw == "/get_rooms":
                    get_rooms()
                elif text[0] == "/add_room":
                    try:
                        add_room(text[1])
                    except:
                        print("Please add a room-name!")
                elif text[0] == "/get_room":
                    try:
                        get_room(text[1])
                    except:
                        print("Please provide a room number when typing this command")
                elif text[0] == "/get_room_users":
                    try:
                        get_room_users(text[1])
                    except:
                        print("Please provide a room number when typing this command")
                elif text[0] == "/join_room":
                    try:
                        add_room_user(text[1])
                    except:
                        print("Please provide a room number when typing this command")
                elif text[0] == "/get_messages":
                    try:
                        get_messages(text[1])
                    except:
                        print(
                            "Please provide a room number to get messages from when typing this command")
                elif text[0] == "/get_user_messages":
                    try:
                        get_user_messages(text[1], text[2])
                    except:
                        print(
                            "Please provide a room number and user ID whn typing this command")
                elif text[0] == "/post_message":
                    try:
                        message = " ".join(text[2:])
                        post_message(text[1], ID, message)
                    except:
                        print(
                            "Please provide a room number and a message when typing this command")
                else:
                    print(
                        "Input was not recognised as a command, type /help for a list of commands")
            elif text[0] == "/connect":
                try:
                    user_id = int(text[1])
                    connect(user_id)
                except:
                    print("Please connect with a user ID")
            elif text[0] == "/register":
                try:
                    add_user(text[1])
                except:
                    print("Please enter a name to register when typing the command")
            elif raw == "/help":
                # Print out a help page for all the commands
                print(HELP_NOT_CONNECTED)
                pass
            else:
                print(
                    "When not connected you can only use the /help, /register or /connect commands")


def start():
    print("###### Client start #######")
    receive = threading.Thread(target=receive_thread)
    send = threading.Thread(target=send_thread)
    receive.start()
    send.start()


start()
