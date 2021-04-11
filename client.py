import requests
import threading
# TODO still quite a bit
BASE = "http://127.0.0.1:5000/api/"
global ID
ID = -1

## USERS #######################################################################

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
    #text = input("Please create a username: ")
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
        # TODO Make the server give their client their ID upon registration
        response = requests.post(BASE + "user/" + user_id, {"id": 1})
        print(response.json())
    else:
        print("Please enter an ID.")

## ROOMS #######################################################################

# TODO: this
def get_rooms():
    pass

# TODO: this
def add_room():
    pass


# TODO: this
def get_room(room_id):
    pass

## ROOM USERS ##################################################################

# TODO: this
def get_room_users():
    pass


# TODO: this
def add_room_user(room_id):
    pass

## MESSAGES ####################################################################

# TODO: this
def get_messages(room_id):
    pass


# TODO: this
def get_user_messages(room_id, user_id):
    pass


# TODO: this
def post_message(room_id, user_id, message):
    pass


# TODO: this
def receiveThread():
    # TODO: Receiving messages and prompts from server.
    pass

## STARTUP #####################################################################


def sendThread():
    while(True):
        raw = input(":")
        text = raw.split(" ")
        # Raw is command only, text[] is command + args
        # TODO Handle index out of bounds
        if raw.startswith("/"):
            if ID >= 0:
                if raw == "/help":
                    # Print out a help page for all the commands
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
                elif text[0] == "/get_rooms":
                    get_rooms()
                elif raw == "/add_room":
                    add_room()
                elif text[0] == "/get_room":
                    get_room(text[1])
                elif text[0] == "/get_room_users":
                    get_room_users()
                elif text[0] == "/join_room":
                    add_room_user(text[1])
                elif text[0] == "/get_messages":
                    get_messages(text[1])
                elif text[0] == "/get_user_messages":
                    get_user_messages(text[1], text[2])
                elif text[0] == "/post_message":
                    message = " ".join(text[2:])
                    post_message(text[1], ID, message)
                else:
                    print("Input was not recognised as a command, type /help for a list of commands")
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
                pass
            else:
                print("When not connected you can only use the /help, /register or /connect commands")


def start():
    print("###### Client start #######")
    recieve = threading.Thread(target=receiveThread)
    send = threading.Thread(target=sendThread)
    recieve.start()
    send.start()

start()
