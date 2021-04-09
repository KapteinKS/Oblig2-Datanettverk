from flask import Flask, url_for, request
from markupsafe import escape

app = Flask(__name__)

userlist = {"Joe", "Bob", "Briggs", "Yo-Yo Ma"}
roomlist = {1,2,3,4,5,6,7}


## FUNCTIONS ######################
###################################

## User-functions

def register_new_user():
    # SHOW REGISTRY FORM
    return "ayo fam whaddup, neue user"

def get_all_users():
    out=""
    for user in userlist:
        out+= "User: " + user + "\n"
    return out

## Room-functions

def add_new_room():
    # SHOW REGISTRY FORM
    return "ayo fam whaddup, new room, innit?"

def rooms():
    out=""
    for room in roomlist:
        out+= "Room: " + str(room) + "\n"
    return out

def get_single_room(room_id):
    return roomlist[room_id+1]


## ROUTING ########################
###################################

## User-routing

@app.route('/api/users')
def users():
    if request.method == 'POST':
        return register_new_user()
    elif request.method == 'GET':
        return get_all_users()

@app.route('/api/user/<user-id>')
def user(user_id):
    if request.method == 'DELETE':
        return delete_user(user_id)
    elif request.method == 'GET':
        return get_single_user(user_id)

## Chat-room routing
@app.route('/api/rooms')
def rooms():
    if request.method == 'POST':
        return add_new_room()
        # add one
    elif request.method == 'GET':
        return get_all_rooms()
        # get all

@app.route('/api/room/<room-id>')
def room(room_id):
    return get_single_room()



#####################
#####################

def do_the_login():
    return "doTheLogin!!!!!!"

def show_the_login_form():
    return "showTheLoginForm......."

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % escape(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %s' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return 'Subpath %s' % escape(subpath)





@app.route('/')
def index():
    return 'index'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()

@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

@app.route('/api/listAll')
def listAll():
    out = ""
    for name in array:
        out += name + " & "
    return out










if __name__ == "__main__":
    app.run(debug=True)
