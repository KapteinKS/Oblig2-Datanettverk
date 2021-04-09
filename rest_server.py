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


def populate():
    users[0] = {"id": 0, "name": "Joe"}  # This should be r1.name
    users[1] = {"id": 1, "name": "Bobby"}
    users[2] = {"id": 2, "name": "Elvira"}

    rooms[0] = {
        "id": 0,
        "name": "General",
        "size": 32,
        "listOfUsers": [0, 1, 2],
        "listOfMessages": [],
    }
    rooms[1] = {
        "id": 1,
        "name": "Memes",
        "size": 32,
        "listOfUsers": [],
        "listOfMessages": [],
    }


populate()


class Users(Resource):
    def get(self):  # return users
        # TODO return list of users in JSON format
        if len(users) == 0:
            abort(404, message="No users registered")
        return list(users.values())

    def put(self):  # add user to db
        # TODO add user to list with auto increment user ID
        print(request.form['name'])
        id = len(users)
        name = request.form['name']
        users[id] = {"id": id, "name": name}
        return "OK", 201


class User(Resource):
    def get(self, user_id):  # return user by user ID
        # TODO get user from list and return in JSON format
        if user_id in users:
            return users[user_id]
        else:
            abort(404, message="No user found with that ID")

    def delete(self, user_id):  # delete user by user ID
        # TODO check user can only delete themselves
        if user_id in users:
            del users[user_id]
            return "OK", 204
        else:
            abort(404, message="No user found with that ID")


class Rooms(Resource):
    def get(self):  # get all rooms
        # TODO get rooms from list and return in JSON format
        if len(rooms) == 0:
            abort(404, message="No rooms created yet")
        else:
            return list(rooms.values())

    def put(self):  # add new room
        # TODO add new room to list with auto incrementing room ID
        return "", 201


class Room(Resource):
    def get(self, room_id):  # get room by room ID
        # TODO get from list and return in JSON format
        if room_id in rooms:
            return rooms[room_id] + "hallo"
        else:
            abort(404, message="No room found with that ID")


class RoomUsers(Resource):
    def get(self, room_id):  # get all user in a room by room ID
        # TODO get users from list, return JSON
        if room_id in rooms:
            out = json.loads(json.dumps(rooms[room_id]))
            return out["listOfUsers"]

            #return str(rooms[room_id])
            #return rooms[room_id].users  # I guess
        else:
            abort(404, message="No room found with that ID")

    def put(self, room_id):  # add user to room by room ID
        # TODO check user is registered, add to room
        if room_id in rooms:
            return "", 201
        else:
            abort(404, message="No room found with that ID")


class Messages(Resource):
    def get(self, room_id):  # get all messages in room by room ID
        # TODO get messages from list, return JSON
        if room_id in rooms:
            return rooms[room_id].messages
        else:
            abort(404, message="No room found with that ID")


class RoomUserMessages(Resource):
    def get(
        self, room_id, user_id
    ):  # get all messages sent in room by user by room ID and user ID
        # TODO check user exists, get messages from list, return JSON
        if room_id in rooms:
            return rooms[room_id].user[user_id].messages
        else:
            abort(404, message="No room found with that ID")

    def post(
        self, room_id, user_id
    ):  # add message from user in room by room ID and user ID
        # TODO check user exists, add new message (str)
        if room_id in rooms:
            return "", 201
        else:
            abort(404, message="No room found with that ID")


api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int:user_id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<int:room_id>")
api.add_resource(RoomUsers, "/api/room/<int:room_id>/users")
api.add_resource(Messages, "/api/room/<int:room_id>/messages")
api.add_resource(RoomUserMessages, "/api/room/<int:room_id>/<int:user_id>/messages")

if __name__ == "__main__":
    app.run(debug=True)
