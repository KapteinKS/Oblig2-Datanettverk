from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


fem = 5


def die(you):
    print(you, "is dead")


def start():
    die("Sander")


start()

if __name__ == "__rest_server__":
    app.run(debug=True)
    