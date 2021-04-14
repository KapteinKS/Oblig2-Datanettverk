import requests
import threading
import time
import re
import socket
import sys
import argparse
import random
from requests.exceptions import HTTPError

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
ALL_COMMANDS = ["/help", "/connect USER_ID", "/register NAME", "/users", "/user USER_ID", "/get_rooms",
                "/add_room ROOM_NAME", "/get_room ROOM_ID",
                "/get_rooms_users ROOM_ID", "/join_room ROOM_ID", "/get_messages ROOM_ID",
                "/get_user_messages ROOM_ID USER_ID", "/post_message ROOM_ID MESSAGE"]


# USERS #######################################################################
# This in the "login" method. Users can type /connect [USER ID] to connect with the specified ID, and the server will
# check to see if the user ID belongs to a registered user
def connect(user_id):
    if requests.get(BASE + "login", {"id": user_id}):
        global ID
        ID = user_id
        print("Connection established, welcome", get_name(user_id) + "!")
        receive = threading.Thread(target=receive_thread, args=[user_id])
        receive.start()
    else:
        print("No user found with that ID")


# This method displays all registered users 
def get_users():  # return users
    response = requests.get(BASE + "users", {"id": 1}).json()
    print("Users:")
    for user in response:
        print("\n" + user["name"])
    return response


# This method adds a new user to the system. It takes a user name and if it is legal 
# according to the regex it will add a new user 
def add_user(user_name):  # add user to db
    # Thank you StackOverflow for naming regex <3
    if re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', user_name):
        response = requests.put(BASE + "users", {"name": user_name}).json()
        print(f"Successfully added new user, with ID: {response}")
        return response
    else:
        print("\nIllegal user name."
              "\nUser name rules: "
              "\n\t1. \tOne or two names"
              "\n\t2. \tUpper case and lower case letters"
              "\n\t3. \tNo special characters"
              "\n\t4. \tName(s) can be 2-25 characters (each)")


# This method returns the entire user as a JSON element
def get_user(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + user_id, {"id": ID}).json()
        print(response["name"])
        return response
    else:
        print("Please use a number")


# This method simply returns the name of a specified user
def get_name(user_id):
    if type(int(user_id)) == int:
        response = requests.get(BASE + "user/" + str(user_id), {"id": ID})
        return response.json()["name"]


# A user can only delete themselves, and if they do the global variable ID 
# will be set to -1, to handle "logging the user out". We also had to use an HTTP post request because 
# the delete request would only take the URL argument, and would give errors when we 
# tried to pass the user ID as a JSON element
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
# This method displays a list of registered rooms, with room name and ID
def get_rooms():
    response = requests.get(BASE + "rooms", {"id": ID})
    for room in response.json():
        print("ID:", str(room["id"]), "\tName:", str(room["name"]),
              "\tNumber of users:", str(room["numberOfUsers"]))
    return response.json()


# This method lets users add new rooms, with a room name, by sending an HTTP put request, and passing the name in a JSON
def add_room(room_name):
    response = requests.put(BASE + "rooms", {"id": ID, "name": room_name})
    text = response.json()
    print(text)
    arr = text.split()
    return arr[3].split(',')[0]


# This method displays which users are registered in a specified room, and the messages that have been sent in that room
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
                    print()
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
# This method displays a list of users registered in a specified room, if the user types /get_room_users [ROOM ID]
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


# By typing /join_room [ROOM NUMBER] the user can become part of a room, and will get 
# access to seeing and adding messages in the specified room
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
# This method ensures a nicely formatted output of messages. 
# It also adds 100 blank lines to always only display the newly gotten messages
def format_messages(response):
    for x in range(101):
        print()  # Clear screen

    users = {}
    for message in response:
        if message["sender"] not in users:
            users[int(message["sender"])] = get_name(int(message["sender"]))
        print("\t" + users[int(message["sender"])], ":",
              "\n\t\t" + message["content"])


# This method send an HTTP get request to the server trying to get all 
# messages in a specified room by adding the room_id to the url
def get_messages(room_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/messages", {"id": ID})
        format_messages(response.json())
        return response.json()


# This method send an HTTP get request to the server trying to get all 
# messages from a specified user in a specified room
def get_user_messages(room_id, user_id):
    if type(int(room_id)) == int:
        response = requests.get(
            BASE + "room/" + room_id + "/" + user_id + "/messages", {"id": ID})
        format_messages(response.json())
        return response.json()


# The user can get a message by message ID, this method will send an HTTP get request
def get_message(message_id):
    if type(int(message_id)) == int:
        response = requests.get(
            BASE + "message/" + str(message_id), {"id": ID})
        print(response.json())
        return response.json()


# The user can post a message in a room they have joined, regardless of currently being attached to it or not
# by typing /post_message [ROOM NUMBER] [MESSAGE]. This method will sent an HTTP post request to the server which will
# then try to add the message
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


# When a user is connected (to a room) it will be viewed as a message and posted in 
# the room they are currently attached to
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
def receive_thread(user_id):
    # TODO: Receiving messages and prompts from server.
    # push notification with message id
    # get message from server
    # show message
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    sock.send(str(user_id).encode())
    while True:
        push = sock.recv(1024)
        print(push.decode() + "push notification test here")
        get_message(int(push.decode()))


# STARTUP #####################################################################
# This method handles input from the user and executes the commands. If the input start with "/" it is recognised
# as the user trying to use a command. If there is no "/" at the start of a line, it is viewed as a message, and
# will be sent if the user is connected with a valid user ID, and connected to a room. There is also a check to see
# if the user is connected, as ID is passed with every request to the server. An unconnected user can only register
# a new user or connect with a valid ID, or ask for help. The /help command also gives different results depending
# on if the user is connected or not
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


# BOT STUFF ###################################################################
# Bots create pre determined rooms, and join the one they created. 
# They do not necessarily join every room, but they can in theory join any room
def join_random():
    rooms = execute("/get_rooms")
    print(f"There are {len(rooms)} rooms")
    room_to_join = random.randint(0, (len(rooms) - 1))
    print(f"You're joining room {room_to_join}")
    time.sleep(0.5)
    execute("/join_room " + str(room_to_join))
    time.sleep(0.5)
    return room_to_join


# Bertram reacts positivly to everyone except Joe, who he hates
def bertram_the_bot():
    botID = execute("/register Bertram")
    time.sleep(1)
    print("ATTEMTING: /connect " + str(botID))
    execute("/connect " + str(botID))
    time.sleep(0.5)
    room_to_join = join_random()
    # execute("/join_room 0")
    time.sleep(0.5)
    execute("/post_message " + str(room_to_join) + " Hello I am Bertram.")
    time.sleep(1)
    # TODO: Put this in a loop, to get responses ####
    msgs = execute("/get_messages " + str(room_to_join))
    joecheck = False;
    rndmsg = random.choice(msgs)
    # TODO: Check that the randomly selected message is not from self
    time.sleep(0.5)
    # Checking if any of the messages is from Joe
    for msg in msgs:
        if get_user(str(msg["sender"]))["name"].lower() == "joe":
            joecheck = True
    if joecheck:
        execute("/post_message " + str(room_to_join) + " Joe, pardon my french, but why don't you just shut the HECK up?!")
    else:
        msg = "Dang " + str(get_user(str(rndmsg["sender"]))["name"]) + ", good point!"
        execute("/post_message " + str(room_to_join) + " " + msg)

    time.sleep(0.5)
    ###########################################
    execute(input("BREAK:"))


# This bot is based on Carlton Banks from The Fresh Prince of Bel Air. It will add a new room called Dancing,
# join this room and send some messages in this room, before joining another room and sending a few more messages there
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
    execute("/join_room 3")
    time.sleep(1)

    execute("/get_room " + room_id)
    for x in range(3):
        time.sleep(60)
        execute(random.choice(messages))
    time.sleep(1)
    execute("I'm gonna join another room now")
    room_to_join = join_random()
    time.sleep(2)
    execute("/get_room " + str(room_to_join))
    for x in range(3):
        time.sleep(90)
        execute(random.choice(messages))


# This bot is a Bob Dylan reference. He will "sing" in his created room, and then go see if it can find Joe
def bobby_the_bot():
    # What's copyright again?
    messages = ["How many roads must a man walk down \nBefore you call him a man? "
                "\nHow many seas must a white dove sail \nBefore she sleeps in the sand? "
                "\nYes, and how many times must the cannonballs fly \nBefore they're forever banned?"
                "\n\nThe answer, my friend, is blowin' in the wind\nThe answer is blowin' in the wind",
                "Once upon a time you dressed so fine \nThrew the bums a dime in your prime, didn't you?"
                "\nPeople call, say 'Beware doll, you're bound to fall' \nYou thought they were all a-kiddin' you"
                "\nYou used to laugh about \nEverybody that was hangin' out"
                "\nNow you don't talk so loud \nNow you don't seem so proud "
                "\nAbout having to be scrounging your next meal    "
                "\n\nHow does it feel? \nHow does it feel? \nTo be without a home? "
                "\nLike a complete unknown? \nLike a rolling stone?",
                "My throat is getting tired, now", "I don't think I can sing anymore",
                "I'm gonna go see if Joe Rogan has said something interesting",
                "Has anyone seen Joe today?", "I wanted to see if he'd said something interesting"]
    botID = execute("/register Robert Zimmerman")
    time.sleep(1)
    print("Connecting")
    execute("/connect " + str(botID))
    time.sleep(1)
    room_id = execute("/add_room The Rolling Thunder Revue")
    time.sleep(1)
    execute("/join_room " + room_id)
    time.sleep(1)
    execute("/get_room " + room_id)
    for x in range(5):
        time.sleep(10)
        execute(messages[x])
    room_to_join = join_random()
    time.sleep(2)
    execute("/get_room " + str(room_to_join))
    time.sleep(10)
    execute(messages[5])
    time.sleep(50)
    execute(messages[6])

# Elvira creates her own room, and posts some Horror-movie facts.
# She waits 10 seconds before starting, in case anybody wants to join her!
def elvira_the_bot():
    trivia_start = ["Did you know, ", "Get this, ", "Fun fact, ","Was you aware that ", "Were you aware, "]
    trivia_content = ["Suspiria was originally written to be about 12 year old girls! ", "Tobe Hooper intenden the Texas Chain-Saw Massacre as a dark comedy! ","Sam Raimi had lost the rights to the Evil Dead when making the sequel, so they had to remake it at the beginning of Evil Dead II! ","Sam Loomis' character in Halloween is named after a character in Psycho! ","Tony Todd had real bees in his mouth for Candyman! ","Stephen King's son appears in the film Creepshow! ","The Crypt Keeper makes an appearance in the family-horror film Casper! ","The Conjuring films are all based on supposedly real events! ", "The Final Destination franchise is based on a scrapped idea for the X-Files! ","The filmmakers behind The Excorcist actually believed in excorcisms, and satanic posessions!"]
    trivia_ending = ["Fascinating, right?","Amazing, I know!","Who'd've thunk it!","I'd've never guessed!","Wow! Incredible!"]
    # Registering Elvira as a user, returning botID.
    botID = execute("/register Elvira")
    time.sleep(2)
    print("BotID: " + str(botID))
    print("Connecting")
    execute("/connect " + str(botID))
    time.sleep(2)
    room_id = execute("/add_room Elvira's Den")
    execute("/join_room " + str(room_id))
    time.sleep(1)
    execute("/post_message " + str(room_id) + " I'll start sharing trivia soon! \U0001F5A4")
    time.sleep(10)
    # Posting a random trivia-fact
    i = 0
    while i < len(trivia_content):
        time.sleep(1)
        execute("/post_message " + str(room_id) + " " + str(random.choice(trivia_start)) + " " + str(trivia_content.pop(random.randint(0,len(trivia_start)))))
        #time.sleep(1)
        #execute("/post_message " + str(room_id) + " " + str(trivia_content.pop(random.randint(0,len(trivia_start)))))
        time.sleep(random.uniform(1.5,3.0))
        execute("/post_message " + str(room_id) + " " + str(random.choice(trivia_ending)))
        i = i+1

    execute("/post_message " + str(room_id) + " " + "This concludes Elvira's trivia showcase! \U0001F578")


# This is a reference to Joe Rogan, the comedian, who will randomly spew inspirational quotes before going
# to the General chat room
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
    for x in range(10):
        execute("/join_room " + str(x))
        time.sleep(0.1)

    execute("/get_room " + str(room_id))
    for x in range(6):
        time.sleep(30)
        execute(random.choice(messages))
    execute("I'm gonna switch to the general chat now now")
    time.sleep(1)
    execute("/get_room 0")
    for x in range(4):
        time.sleep(60)
        execute(random.choice(messages))

################################################################################

def start():
    print("###### Client start #######")
    send = threading.Thread(target=send_thread)
    send.start()
    if BOTNAME is not None:
        if BOTNAME.lower() == "bertram":
            bertram_the_bot()
        elif BOTNAME.lower() == "carlton":
            carlton_the_bot()
        elif BOTNAME.lower() == "joe":
            joe_the_bot()
        elif BOTNAME.lower() == "bobby":
            bobby_the_bot()
        elif BOTNAME.lower() == "elvira":
            elvira_the_bot()


start()
