from flask import Flask
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
    r1 = {
        "id": 1,
        "name": "General",
        "size": 32,
        "listOfUsers": [1, 2, 3],
        "listOfMessages": [],
    }
    r2 = {
        "id": 2,
        "name": "Memes",
        "size": 32,
        "listOfUsers": [],
        "listOfMessages": [],
    }

    users[1] = {"id": 1, "name": "Joe"}  # This should be r1.name
    users[2] = {"id": 2, "name": "Bobby"}
    users[3] = {"id": 3, "name": "Elvira"}

    rooms[1] = {
        "id": 1,
        "name": "General",
        "size": 32,
        "listOfUsers": [1, 2, 3],
        "listOfMessages": [],
    }
    rooms[2] = {
        "id": 2,
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
        return users


class Rooms(Resource):
    def get(self):  # get all rooms
        # TODO get rooms from list and return in JSON format
        if len(rooms) == 0:
            abort(404, message="No rooms created yet")
        else:
            return rooms


api.add_resource(Users, "/api/users")
api.add_resource(Rooms, "/api/rooms")

if __name__ == "__main__":
    app.run(debug=True)
