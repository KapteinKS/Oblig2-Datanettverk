from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

users = []


class Users(Resource):
    def get(self): # return users

    def post(self): # users.add

class User(Resource):
    def get(self): # return user

    def post(self): # delete

class Rooms(Resource):
    def get(self): # get all
        
    def post(self): # add one
        
class Room(Resource):
    def get(self): # get room
        
class RoomUsers(Resource):
    def get(self): # get all
    
    def post(self): # add one
        
class Messages(Resource):
    def get(self): # get all
        
class RoomUserMessages(Resource):
    def get(self): # get all
        
    def post(self): # add one
        
api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<user-id>")
api.add_resource(Rooms, "/api/rooms")
api.add_resource(Room, "/api/room/<room-id")
api.add_resource(RoomUsers, "/api/room/<room-id>/users")
api.add_resource(Messages, "/api/room/<room-id>/messages")
api.add_resource(RoomUserMessages, "/api/room/<room-id/<user-id/messages")

if __name__ == "__main__":
    app.run(debug=True)
