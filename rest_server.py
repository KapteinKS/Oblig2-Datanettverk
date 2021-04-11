from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
import json

app = Flask(__name__)
api = Api(app)

# user: id, name
# room: id, , name, size, listOfUsers, listOfMessages
# msg: senderid, text
users = {}
rooms = {}
messages = {}


def getMessagesInRoom(room_id):
    room_messages = (
        filter(lambda message: message["room"] == room_id, messages.values())
        if len(messages) > 0
        else []
    )
    return list(room_messages)


def addMessage(self, room_id, user_id):
    messages[len(messages)] = {
        "id": len(messages),
        "room": room_id,
        "sender": user_id,
        "content": str(self),
    }


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
        "listOfMessages": getMessagesInRoom(0),
    }
    rooms[1] = {
        "id": 1,
        "name": "Memes",
        "size": 32,
        "listOfUsers": [1],
        "listOfMessages": getMessagesInRoom(1),
    }

    addMessage("HELLO THIS IS A MESSAGE ADDED LATER", 1, 2)
    addMessage("HELLO THIS IS A NEW MESSAGE ADDED LATER", 0, 2)


populate()

user_delete_args = reqparse.RequestParser()
user_delete_args.add_argument(
    "id", type=int, help="ID of current user", required=True)


def get_room_users(room_orig):
    room_users = []
    for user_id in room_orig["listOfUsers"]:
        room_users.append(users[user_id])
    return room_users


class Users(Resource):
    def get(self):  # return users
        if len(users) == 0:
            return []
        return list(users.values())

    def put(self):  # add user
        id = len(users)
        name = request.form["name"]
        users[id] = {"id": id, "name": name}
        return "OK", 201


class User(Resource):
    def get(self, user_id):  # return user by user ID
        if user_id in users:
            return users[user_id]
        else:
            abort(404, message="No user found with that ID")

    # had to hack this method and use post instead of delete as delete would not accept a JSON element 
    def post(self, user_id):
        args = user_delete_args.parse_args()
        if user_id not in users:
            abort(404, message="No user found with that ID")
        if user_id != args["id"]:
            abort(403, message="You do not have permission to delete another user")

        del users[user_id]
        return "OK", 204


class Rooms(Resource):
    def get(self):  # get all rooms
        if len(rooms) == 0:
            return []
        else:
            room_list = []
            for room_orig in rooms.values():
                room = room_orig.copy()
                room["numberOfUsers"] = len(room["listOfUsers"])
                del room["listOfUsers"]
                del room["listOfMessages"]
                room_list.append(room)
            return room_list

    def put(self):  # add new room
        id = len(rooms)
        name = request.form["name"]
        rooms[id] = {
            "id": id,
            "name": name,
            "size": 32,
            "listOfUsers": [],
            "listOfMessages": [],
        }
        return "OK", 201


class Room(Resource):
    def get(self, room_id):  # get room by room ID
        if room_id in rooms:
            room = rooms[room_id].copy()

            # Get full user dicitonaries, or empty list if empty
            room["listOfUsers"] = get_room_users(room) if len(room["listOfUsers"]) > 0 else []
            # Get messages as list, or empty list if emtpy
            room["listOfMessages"] = list(room["listOfMessages"].values()) if len(room["listOfMessages"]) > 0 else []
            return room
        else:
            abort(404, message="No room found with that ID")


class RoomUsers(Resource):
    def get(self, room_id):  # get all user in a room by room ID
        if room_id in rooms:
            out = json.loads(json.dumps(rooms[room_id]))
            if len(get_room_users(out)) > 0:
                return get_room_users(out)
            else:
                return "No users added yet"
        else:
            abort(404, message="Room not found")

    def put(self, room_id):  # add user to room by room ID
        if room_id in rooms:
            user_id = int(request.form["id"])
            if user_id in users:
                room = rooms[room_id]
                room["listOfUsers"].append(user_id)
                return "OK", 201
            abort(404, message="No user found with that ID")
        else:
            abort(404, message="No room found with that ID")


class Messages(Resource):
    def get(self, room_id):  # get all messages in room by room ID
        if room_id in rooms:
            return getMessagesInRoom(room_id)

        else:
            abort(404, message="No room found with that ID")


class RoomUserMessages(Resource):
    def get(
        self, room_id, user_id
    ):  # get all messages sent in room by user by room ID and user ID
        if room_id in rooms and user_id in users:
            room_messages = getMessagesInRoom(room_id)
            this_rooms_users_msgs = filter(
                lambda message: message["sender"] == user_id, room_messages
            )
            return list(this_rooms_users_msgs)

        else:
            abort(404, message="COULDN'T FIND ROOM OR USER")

    def post(
        self, room_id, user_id
    ):  # add message from user in room by room ID and user ID
        if room_id in rooms:
            room = rooms[room_id]
            if user_id in room["listOfUsers"]:
                message = request.form["message"]
                addMessage(message, room_id, user_id)
                return "OK", 201
            else:
                abort(404, message="That user is not registered to this room")
        else:
            abort(404, message="No room found with that ID")


api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int:user_id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<int:room_id>")
api.add_resource(RoomUsers, "/api/room/<int:room_id>/users")
api.add_resource(Messages, "/api/room/<int:room_id>/messages")
api.add_resource(RoomUserMessages,
                 "/api/room/<int:room_id>/<int:user_id>/messages")

if __name__ == "__main__":
    app.run(debug=True)
