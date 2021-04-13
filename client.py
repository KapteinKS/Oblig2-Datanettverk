import requests
import threading
import time
import re
import socket
from requests.exceptions import HTTPError
# TODO Thread
BASE = "http://127.0.0.1:5000/api/"
ID = -1
ROOM = -1
ADDRESS = ("127.0.0.1", 5001)

HELP_CONNECTED = """
| /users                                 gives a list of users.
| /user <id>                             gives the user.
| /delete <id>                           deletes the user. You can only delete your own account.
| /get_rooms                             gives a list of chatrooms.
| /add_room <name>                       creates a new room.
| /get_room <room_id>                    gives a room(???).
| /get_room_users <room_id>              gives all the users in a room.
| /join_room <room_id>                   joins a new room.
| /get_messages <room_id>                gives all the messages of a room.
| /get_user_messages <room_id> <user_id> gives the messages of a user from a specific room.
| /post_message <room_id> <message>      posts a message in a specific room."""
HELP_NOT_CONNECTED = """When not connected you can only use the /help, /register or /connect
commands. Please register as a new user then connect with your given ID.
Use /register <name> and then /connect <id>."""
ALL_COMMANDS = ["/help", "/connect USER_ID", "/register NAME", "/users", "/user USER_ID", "/get_rooms", "/add_room ROOM_NAME", "/get_room ROOM_ID",
                "/get_rooms_users ROOM_ID", "/join_room ROOM_ID", "/get_messages ROOM_ID", "/get_user_messages ROOM_ID USER_ID", "/post_message ROOM_ID MESSAGE"]
# USERS #######################################################################


def connect(user_id):
    if requests.get(BASE + "login", {"id": user_id}):
        global ID
        ID = user_id
        print("Connection established, welcome", get_name(user_id) + "!")
    else:
        print("No user found with that ID")


def get_users():  # return users
    response = requests.get(BASE + "users", {"id": 1}).json()
    print("Users:")
    for user in response:
        print("\n" + user["name"])


def add_user(user_name):  # add user to db
    # Thank you StackOverflow <3
    if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', user_name):
        response = requests.put(BASE + "users", {"name": user_name}).json()
        print(f"Successfully added new user, with ID: {response}")
        return(response)
    else:
        print("\nIllegal user name."
              "\nUser name rules: "
              "\n\t1. \tOne or two names"
              "\n\t2. \tUpper case and lower case letters"
              "\n\t3. \tNo special characters"
              "\n\t4. \tName(s) can be 2-25 characters (each)")


def get_user(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + user_id, {"id": ID}).json()
        print(response["name"])
    else:
        print("Please use a number")


def get_name(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + str(user_id), {"id": ID})
        return response.json()["name"]


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
    for room in response.json():
        print("ID:", str(room["id"]), "\tName:", str(room["name"]),
              "\tNumber of users:", str(room["numberOfUsers"]))


def add_room(room_name):
    response = requests.put(BASE + "rooms", {"id": ID, "name": room_name})
    print(response.json())


def get_room(room_id):
    if type(int(room_id)) == int:
        try:
            list_of_globals = globals()
            list_of_globals['ROOM'] = int(room_id)
            response = requests.get(BASE + "room/" + str(room_id), {"id": ID})
            if response.status_code != 404:
                full = response.json()
                for x in range(50):
                    print()  # Clear screen
                users = full["listOfUsers"]
                messages = full["listOfMessages"]
                print("\nName:", full["name"])
                print("\nUsers:")
                for user in users:
                    print("\t" + user["name"])
                print("\nMessages:")
        
                names = {}
                for message in messages:
                    if message["sender"] not in names:
                        names[int(message["sender"])] = get_name(int(message["sender"]))
                    print("\t" + names[int(message["sender"])], ":", "\t" + message["content"])
            else:
                raise HTTPError
        except HTTPError:
            print("No room found with that ID", room_id)
    else:
        print("Please use a number")

# ROOM USERS ##################################################################


def get_room_users(room_id):
    if type(int(room_id)) == int:
        # "/api/room/<int:room_id>/users"
        response = requests.get(
            BASE + "room/" + str(room_id) + "/users", {"id": ID})
        print(f"Users in Room {room_id}:")
        for usr in response.json():
            print("UserID:", str(usr["id"]), "\tName:", str(usr["name"]))
    else:
        print("Please use a number")


def add_room_user(room_id):
    # "/api/room/<int:room_id>/users"
    if type(int(room_id)) == int:
        print("You made it, congratulations friend.")
        response = requests.put(
            BASE + "room/" + str(room_id) + "/users", {"id": ID})
        print(response.json())
    else:
        print("Please usa a number")

# MESSAGES ####################################################################


def format_messages(response):
    for x in range(101):
        print()  # Clear screen

    users = {}
    for message in response:
        if message["sender"] not in users:
            users[int(message["sender"])] = get_name(int(message["sender"]))
        print(users[int(message["sender"])], ":", message["content"])


def get_messages(room_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/messages", {"id": ID})
        format_messages(response.json())


def get_user_messages(room_id, user_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/" + user_id + "/messages", {"id": ID})
        format_messages(response.json())


def get_message(message_id):
    if type(int(message_id)) == int:
        response = requests.get(
            BASE + "message/" + message_id, {"id": ID})
        print(response.json)


def post_message(room_id, message):
    if type(int(room_id)) == int:
        user_id = ID
        url = BASE + "room/" + str(room_id) + "/" + str(user_id) + "/messages"
        response = requests.post(url, {"id": ID, "message": message})
        if response.json() == "OK":
            get_messages(room_id)
        else:
            # Should be rare, as many other things need to fail to reach this
            print("Message was not sent")


def post_message_in_room(message):
    url = BASE + "room/" + str(ROOM) + "/" + str(ID) + "/messages"
    response = requests.post(url, {"id": ID, "message": message})
    if response.json() == "OK":
        get_room(ROOM)


# TODO: this
def receive_thread():
    # TODO: Receiving messages and prompts from server.
    # push notification with message id
    # get message from server
    # show message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    msg = "1"
    sock.send(msg.encode())

# STARTUP #####################################################################


def execute():
    raw = input()
    text = raw.split(" ")
    # Raw is command only, text[] is command + args
    if raw.startswith("/"):
        if ID >= 0:
            if raw == "/help":
                # Print out a help page for all the commands
                print(HELP_CONNECTED)
                pass
            elif raw == "/users":
                return get_users()

            elif text[0] == "/user":
                try:
                    return get_user(text[1])
                except:
                    print("Please enter a user to get when typing the command")
            elif text[0] == "/delete":
                try:
                    return delete_user(text[1])
                except:
                    "Please enter a user to delete when typing the command"
            elif raw == "/get_rooms":
                return get_rooms()
            elif text[0] == "/add_room":
                try:
                    return add_room(text[1])
                except:
                    print("Please add a room-name!")
            elif text[0] == "/get_room":
                try:
                    return get_room(text[1])
                except:
                    print("Please provide a room number when typing this command")
            elif text[0] == "/get_room_users":
                try:
                    return get_room_users(text[1])
                except:
                    print("Please provide a room number when typing this command")
            elif text[0] == "/join_room":
                try:
                    return add_room_user(text[1])
                except:
                    print("Please provide a room number when typing this command")
            elif text[0] == "/get_messages":
                try:
                    return get_messages(text[1])
                except:
                    print(
                        "Please provide a room number to get messages from when typing this command")
            elif text[0] == "/get_user_messages":
                try:
                    return get_user_messages(text[1], text[2])
                except:
                    print("Please connect with a user ID")
            else:
                print("Input was not recognised as a command")
        # elif text[0] == "/register":
        #    try:
        #        message = " ".join(text[2:])
        #        return post_message(text[1], message)
        #    except:
        #        print("Please enter a name to register when typing the command")
        elif raw == "/help":
            # Print out a help page for help on how to get started
            print(HELP_NOT_CONNECTED)
            print("Here's a list of all the commands: ")
            for command in ALL_COMMANDS:
                print(command)
            pass
        
        elif text[0] == "/connect":
            try:
                user_id = int(text[1])
                connect(user_id)
            except:
                print("Please connect with a user ID")
        elif text[0] == "/register":
            try:
                return add_user(" ".join(text[1:]))
            except:
                print("Please enter a name to register when typing the command")
        else:
            print(
                "When not connected you can only use the /help, /register or /connect commands")
    elif ID >= 0 and ROOM >= 0:
        if len(raw) > 0:
            post_message_in_room(raw)
            print("Input was not recognised as a command, type /help for a list of commands")
    else:
        print("Input was not recognised as a command, or message was not sent as you may not be"
              " logged in, or connected to a room."
              "\nType /help for a list of commands")


def send_thread():
    execute()
    # while True:
        # bertramTheBot()
    #    pass


## BOT STUFF ###################################################################

def bertramTheBot():
    botID = execute("/register Bertram")
    time.sleep(0.5)
    print("ATTEMTING: /connect "+str(botID))
    time.sleep(0.5)
    execute("/connect "+str(botID))
    time.sleep(0.5)
    execute("/join_room 0")
    time.sleep(0.5)
    #execute("/join_room 0")
    #time.sleep(0.5)
    execute("/post_message 0 Hello I am Bertram.")
    time.sleep(1.5)
    execute(input("BREAK:"))
    #pass


################################################################################


def start():
    print("###### Client start #######")
    receive = threading.Thread(target=receive_thread)
    send = threading.Thread(target=send_thread)
    receive.start()
    send.start()


start()
