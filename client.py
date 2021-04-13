import requests
import threading
import time
import re
import socket
import sys
import argparse
import random
from requests.exceptions import HTTPError
# TODO Thread
parser = argparse.ArgumentParser()
parser.add_argument("-b", type=str)
args = parser.parse_args()

BASE = "http://127.0.0.1:5000/api/"
ID = -1
ROOM = -1
ADDRESS = ("127.0.0.1", 5001)
BOTNAME = args.b
print(BOTNAME)

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
    return response


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
        return response
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
    return response.json()


def add_room(room_name):
    response = requests.put(BASE + "rooms", {"id": ID, "name": room_name})
    text = response.json()
    print(text)
    arr = text.split()
    return arr[3].split(',')[0]


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
                        names[int(message["sender"])] = get_name(
                            int(message["sender"]))
                    print("\t" + names[int(message["sender"])],
                          ":", "\n\t\t" + message["content"])
                return response.json()
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
        return response.json()
    else:
        print("Please use a number")


def add_room_user(room_id):
    # "/api/room/<int:room_id>/users"
    if type(int(room_id)) == int:
        print("You made it, congratulations friend.")
        response = requests.put(
            BASE + "room/" + str(room_id) + "/users", {"id": ID})
        print(response.json())
        return response.json()
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
        print("\t" + users[int(message["sender"])], ":",
              "\n\t\t" + message["content"])


def get_messages(room_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/messages", {"id": ID})
        format_messages(response.json())
        return response.json()


def get_user_messages(room_id, user_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/" + user_id + "/messages", {"id": ID})
        format_messages(response.json())
        return response.json()


def get_message(message_id):
    if type(int(message_id)) == int:
        response = requests.get(
            BASE + "message/" + message_id, {"id": ID})
        print(response.json())
        return response.json()


def post_message(room_id, message):
    if type(int(room_id)) == int:
        user_id = ID
        url = BASE + "room/" + str(room_id) + "/" + str(user_id) + "/messages"
        response = requests.post(url, {"id": ID, "message": message})
        try:
            if response.status_code == 403 or response.status_code == 404:
                raise HTTPError
            else:
                get_messages(room_id)
        except HTTPError:
            print(response.json()["message"])
    else:
        # Should be rare, as many other things need to fail to reach this
        print("Message was not sent")


def post_message_in_room(message):
    url = BASE + "room/" + str(ROOM) + "/" + str(ID) + "/messages"
    response = requests.post(url, {"id": ID, "message": message})
    try:
        if response.status_code == 403 or response.status_code == 404:
            raise HTTPError
        else:
            get_room(ROOM)
    except HTTPError:
        print(response.json()["message"])


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
    push = sock.recv(1024)
    print(push.decode() + "push notification test here")

# STARTUP #####################################################################


def execute(commando):
    raw = commando
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
                    return add_room(" ".join(text[1:]))
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
            elif text[0] == "/post_message":
                try:
                    message = " ".join(text[2:])
                    return post_message(text[1], message)
                except:
                    print(
                        "Please provide a room number and a message when using this command")
            else:
                print("Input was not recognised as a command")
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
    else:
        print("Input was not recognised as a command, or message was not sent as you may not be"
              " logged in, or connected to a room."
              "\nType /help for a list of commands")


def send_thread():
    while True:
        execute(input(":"))
    # bertramTheBot()
#    pass

        ## BOT STUFF ###################################################################
def join_random():
    rooms = execute("/get_rooms")
    print(f"There are {len(rooms)} rooms")
    room_to_join = random.randint(0, (len(rooms)-1))
    print(f"You're joining room {room_to_join}")
    time.sleep(0.5)
    execute("/join_room "+str(room_to_join))
    time.sleep(0.5)
    return room_to_join

def bertram_the_bot():
    botID = execute("/register Bertram")
    time.sleep(1)
    print("ATTEMTING: /connect "+str(botID))
    execute("/connect " + str(botID))
    time.sleep(0.5)
    print("You are here")
    room_to_join = join_random()
    #execute("/join_room 0")
    time.sleep(0.5)
    execute("/post_message " + str(room_to_join) + " Hello I am Bertram.")
    time.sleep(1)

    # Put this in a loop, to get responses ####

    msgs = execute("/get_messages " +str(room_to_join))
    joecheck = False;
    rndmsg = random.choice(msgs)
    for msg in msgs:
        if get_user(str(msg["sender"]))["name"].lower() == "joe":
            joecheck = True
    if joecheck:
        execute("/post_message " +str(room_to_join) + " Joe, why don't you just shut the f*** up?")
    else:

        msg = "Dang " + str(get_user(rndmsg["sender"])["name"]) + ", good point!"
        execute("/post_message " + str(room_to_join) + " " + msg)

    time.sleep(0.5)
    #if (msgs)

    ###########################################

    execute(input("BREAK:"))
    # pass


def carlton_the_bot():
    messages = ["Let's dance!", "Do the Carlton!", "What's a nine-letter word for terrific? Will Smith!",
                "Forget the harlem shake, forget Gangam style, it's time to bring back the CARLTON",
                "Why so glum, chum?"]
    botID = execute("/register Carlton Banks")
    time.sleep(1)
    print("Connecting")
    execute("/connect " + str(botID))
    time.sleep(1)
    room_id = execute("/add_room Dancing")
    time.sleep(1)
    execute("/join_room 0")
    time.sleep(1)
    execute("/join_room " + room_id)
    time.sleep(1)
    execute("/get_room " + room_id)
    for x in range(3):
        execute(random.choice(messages))
        time.sleep(60)
    join_random()
    execute(random.choice(messages))


def bobby_the_bot():
    pass


def elvira_the_bot():
    pass


def joe_the_bot():
    messages = ["Be the hero of your own story.", "If you are the greatest, why would you go around talking about it?",
                "People love to see people fall.", "Fuel yourself with the f*** ups.", "Choose To Be Inspired."]
    botID = execute("/register Joe Rogan")
    time.sleep(1)
    print("Connecting")
    execute("/connect " + str(botID))
    time.sleep(1)
    room_id = execute("/add_room Inspirational Quotes")
    execute("/join_room " + room_id)
    time.sleep(1)
    for x in range(5):
        execute("/join_room " + str(x))
        time.sleep(0.1)
    execute("/get_room " + str(room_id))
    for x in range(6):
        execute(random.choice(messages))
        time.sleep(30)


################################################################################


def start():
    print("###### Client start #######")
    receive = threading.Thread(target=receive_thread)
    send = threading.Thread(target=send_thread)
    receive.start()
    send.start()
    if BOTNAME != None:
        if BOTNAME.lower() == "bertram":
            bertram_the_bot()
        elif BOTNAME.lower() == "carlton":
            carlton_the_bot()
        elif BOTNAME.lower() == "joe":
            joe_the_bot()


start()
