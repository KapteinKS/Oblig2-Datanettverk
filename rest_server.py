from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = {}
rooms = {}


class Users(Resource):
    def get(self): # return users
        return users
    
    def post(self): # users.add

class User(Resource):
    def get(self, user_id): # return user
        return users[user_id]
    
    def post(self, user_id): # delete
        del users[user_id]
        return "OK"
    
class Rooms(Resource):
    def get(self): # get all
        return rooms
        
    def post(self): # add one
        
class Room(Resource):
    def get(self, room_id): # get room
        return rooms[room_id]
    
class RoomUsers(Resource):
    def get(self, room_id): # get all
    
    def post(self, room_id): # add one
        
class Messages(Resource):
    def get(self, room_id): # get all
        
class RoomUserMessages(Resource):
    def get(self, room_id, user_id): # get all
        
    def post(self): # add one
        
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int: user_id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<int: room_id")
api.add_resource(RoomUsers, "/api/room/<int: room_id>/users")
api.add_resource(Messages, "/api/room/<int: room_id>/messages")
api.add_resource(RoomUserMessages, "/api/room/<int: room_id/<int: user_id/messages")

if __name__ == "__main__":
    app.run(debug=True)
