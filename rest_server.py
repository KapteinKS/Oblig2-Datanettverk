from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import json
import threading
import socket
from collections import deque
ADDRESS = ("127.0.0.1", 5001)

app = Flask(__name__)
api = Api(app)

# user: id, name
# room: id, , name, size, listOfUsers, listOfMessages
# msg: senderid, text
users = {}
rooms = {}
messages = {}
user_sockets = {}
message_push_queue = deque()


def get_messages_in_room(room_id):
    room_messages = (
        filter(lambda message: message["room"] == room_id, messages.values())
        if len(messages) > 0
        else []
    )
    return list(room_messages)


def add_message(self, room_id, user_id):
    message_id = len(messages)
    message = {
        "id": message_id,
        "room": room_id,
        "sender": user_id,
        "content": str(self),
    }
    messages[message_id] = message
    message_push_queue.append(message)
    print(f"Pushed to queue message {message['id']}")


def populate():

    users[0] = {
        "id": 0,
        "name": "Joe",
    }
    users[1] = {
        "id": 1,
        "name": "Bobby",
    }
    users[2] = {
        "id": 2,
        "name": "Elvira",
    }

    messages[0] = {
        "id": 0,
        "room": 0,
        "sender": 1,
        "content": "THIS IS A Bobby MESSAGE",
    }
    messages[1] = {
        "id": 1,
        "room": 0,
        "sender": 0,
        "content": "Cowabunga, mydudes!! Joe sent this.",
    }
    messages[2] = {
        "id": 2,
        "room": 0,
        "sender": 1,
        "content": "You're such a dweeb, Joey-Ol'-boy. Love, Bob.",
    }
    messages[3] = {
        "id": 3,
        "room": 1,
        "sender": 2,
        "content": "Je suis Elvira..",
    }
    messages[4] = {
        "id": 4,
        "room": 0,
        "sender": 1,
        "content": "Bobby REPORTING in",
    }

    rooms[0] = {
        "id": 0,
        "name": "General",
        "size": 32,
        "listOfUsers": [0, 1, 2],
    }
    rooms[1] = {
        "id": 1,
        "name": "Memes",
        "size": 32,
        "listOfUsers": [1],
    }

    add_message("HELLO THIS IS A MESSAGE ADDED LATER", 1, 2)
    add_message("HELLO THIS IS A NEW MESSAGE ADDED LATER", 0, 2)


populate()

# user_delete_args = reqparse.RequestParser()
# user_delete_args.add_argument("id", type=int, help="ID of current user", required=True)


def get_room_users(room_orig):
    room_users = []
    for user_id in room_orig["listOfUsers"]:
        room_users.append(users[user_id])
    return room_users


def user_exist(index):
    return index < len(users)


def check_user_valid_get():
    if request.args.get("id") is None or not user_exist(int(request.args.get("id"))):
        abort(
            401,
            message="You must be logged in as a registered user to use this function",
        )
    else:
        return True


def check_user_valid_form():
    if request.form["id"] is None or not user_exist(int(request.form["id"])):
        abort(
            401,
            message="You must be logged in as a registered user to use this function",
        )
    else:
        return True


class Login(Resource):
    def get(self):
        if check_user_valid_get():
            return True
        else:
            return False


class Users(Resource):
    def get(self):  # return users
        if check_user_valid_get():
            if len(users) == 0:
                return []
            return list(users.values())

    def put(self):  # add user
        max = 0
        for user in users:
            if user > int(max):
                max = int(user)
        id = max + 1
        name = request.form["name"]
        users[id] = {"id": id, "name": name}
        return f"{id}", 201


class User(Resource):
    def get(self, user_id):  # return user by user ID
        if check_user_valid_get():
            if user_id in users:
                return users[user_id]
            else:
                abort(404, message="No user found with that ID")

    # had to hack this method and use post instead of delete as delete would not accept a JSON element
    def post(self, user_id):
        # args = user_delete_args.parse_args()
        if check_user_valid_form():
            if user_id not in users:
                abort(404, message="No user found with that ID")
            elif int(user_id) != int(request.form["id"]):
                abort(403, message="You do not have permission to delete another user")

        del users[user_id]
        return "User deleted", 201


class Rooms(Resource):
    def get(self):  # get all rooms
        if check_user_valid_get():
            if len(rooms) == 0:
                return []
            else:
                room_list = []
                for room_orig in rooms.values():
                    room = room_orig.copy()
                    room["numberOfUsers"] = len(room["listOfUsers"])
                    del room["listOfUsers"]
                    room_list.append(room)
                return room_list

    def put(self):  # add new room
        if check_user_valid_form():
            id = len(rooms)
            name = request.form["name"]
            rooms[id] = {
                "id": id,
                "name": name,
                "size": 32,
                "listOfUsers": [],
            }
            return f"Room added, ID: {id}, Name: {name}", 201


class Room(Resource):
    def get(self, room_id):  # get room by room ID
        if check_user_valid_get():
            if room_id in rooms:
                room = rooms[room_id].copy()

                # Get full user dicitonaries, or empty list if empty
                room["listOfUsers"] = get_room_users(
                    room) if len(room["listOfUsers"]) > 0 else []
                # Get messages as list, or empty list if emtpy
                room["listOfMessages"] = get_messages_in_room(room_id)
                return room
            else:
                abort(404, message="No room found with that ID")


class RoomUsers(Resource):
    def get(self, room_id):  # get all user in a room by room ID
        if check_user_valid_get():
            if room_id in rooms:
                if len(rooms[room_id]["listOfUsers"]) > 0:
                    return get_room_users(rooms[room_id])
                else:
                    return "No users added yet"
            else:
                abort(404, message="Room not found")

    def put(self, room_id):  # add user to room by room ID
        if check_user_valid_form():
            if room_id in rooms:
                user_id = int(request.form["id"])
                if user_id in users:
                    room = rooms[room_id]
                    if not user_id in room["listOfUsers"]:
                        # No duplicates, can only join a room once
                        room["listOfUsers"].append(user_id)
                    return "OK", 201
                abort(404, message="No user found with that ID")
            else:
                abort(404, message="No room found with that ID")


class Messages(Resource):
    def get(self, room_id):  # get all messages in room by room ID
        if check_user_valid_get():
            if room_id in rooms:
                return get_messages_in_room(room_id)

            else:
                abort(404, message="No room found with that ID")


class Message(Resource):
    def get(self, message_id):  # get all messages in room by room ID
        if check_user_valid_get():
            if message_id in messages:
                return messages[message_id]

            else:
                abort(404, message="No message found with that ID")


class RoomUserMessages(Resource):
    def get(self, room_id, user_id):  # get all messages sent in room by user by room ID and user ID
        if check_user_valid_get():
            if room_id in rooms and user_id in users:
                room_messages = get_messages_in_room(room_id)
                this_rooms_users_msgs = filter(
                    lambda message: message["sender"] == user_id, room_messages
                )
                return list(this_rooms_users_msgs)

            else:
                abort(404, message="Couldn't find room or user")

    def post(self, room_id, user_id):  # add message from user in room by room ID and user ID
        if check_user_valid_form():
            if room_id in rooms:
                if user_id != int(request.form["id"]):
                    abort(403, message="Cannot submit message on behalf of other users")
                if user_id in rooms[room_id]["listOfUsers"]:
                    message = request.form["message"]
                    add_message(message, room_id, user_id)
                    return "OK", 201
                else:
                    abort(403, message="User is not in this room")
            else:
                abort(404, message="No room found with that ID")


api.add_resource(Login, "/api/login")
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int:user_id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<int:room_id>")
api.add_resource(RoomUsers, "/api/room/<int:room_id>/users")
api.add_resource(Messages, "/api/room/<int:room_id>/messages")
api.add_resource(Message, "/api/message/<int:message_id>")
api.add_resource(RoomUserMessages,
                 "/api/room/<int:room_id>/<int:user_id>/messages")


def accept_connection(sock):
    while True:
        client, address = sock.accept()
        user_id = int(client.recv(1024).decode())
        print(f"User {user_id} connected to push server")
        user_sockets[user_id] = client


def push_notification():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(ADDRESS)
    sock.listen(1)

    push_accept_thread = threading.Thread(
        target=accept_connection, args=[sock])
    push_accept_thread.start()
    # TODO Separate socket creation from push handling, prevent eternal loop
    while True:
        try:
            message = message_push_queue.popleft()
            print("Sending")
            print()
            users = rooms[message["room"]]["listOfUsers"]
            for user in users:
                if user != message["sender"] and user in user_sockets:
                    print(
                        f"Sending push for message {message['id']} to user {user}")
                    user_sockets[user].send(message["id"].encode())
                else:
                    print("Noe er feil med push notification")
        except IndexError:
            # No messages to send
            pass


if __name__ == "__main__":
    push_thread = threading.Thread(target=push_notification)
    push_thread.start()
    app.run(debug=True)
