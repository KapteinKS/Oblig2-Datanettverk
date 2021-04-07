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

if __name__ == "__main__":
    app.run(debug=True)
