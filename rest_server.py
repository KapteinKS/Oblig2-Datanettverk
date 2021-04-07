from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

#TODO imlpement db
users = {}
rooms = {}


class Users(Resource):
    def get(self): # return users
        #TODO return list of users in JSON format
        return users
    
    def put(self): # add user to db
        #TODO add user to db with auto increment user ID

class User(Resource):
    def get(self, user_id): # return user by user ID
        #TODO get user from db and return in JSON format
        return users[user_id]
    
    def delete(self, user_id): # delete user by user ID
        #TODO check user exists, check user can only delete themselves
        del users[user_id]
        return "OK"
    
class Rooms(Resource):
    def get(self): # get all rooms
        #TODO get rooms from db and return in JSON format
        return rooms
        
    def put(self): # add new room
        #TODO add new room to db with auto incrementing room ID
        
class Room(Resource):
    def get(self, room_id): # get room by room ID
        #TODO check room exists, get from db and return in JSON format
        return rooms[room_id]
    
class RoomUsers(Resource):
    def get(self, room_id): # get all user in a room by room ID
        #TODO check room exists, get users from db, return JSON
    
    def put(self, room_id): # add user to room by room ID
        #TODO check room exists, check user is registered, add to room
        
class Messages(Resource):
    def get(self, room_id): # get all messages in room by room ID
        #TODO check room exists, get messages from db, return JSON
        
class RoomUserMessages(Resource):
    def get(self, room_id, user_id): # get all messages sent in room by user by room ID and user ID
        #TODO check room exists, check user exists, get messages from db, return JSON
        
    def post(self): # add message from user in room by room ID and user ID
        #TODO check room exists, check user exists, add new message (str)
        
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int: user_id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<int: room_id")
api.add_resource(RoomUsers, "/api/room/<int: room_id>/users")
api.add_resource(Messages, "/api/room/<int: room_id>/messages")
api.add_resource(RoomUserMessages, "/api/room/<int: room_id/<int: user_id/messages")

if __name__ == "__main__":
    app.run(debug=True)
