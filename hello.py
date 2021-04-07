from flask import Flask
app = Flask(__name__)

array = {"Joe", "Bob", "Briggs"}

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World!'

@app.route('/api/listAll')
def listAll():
    out = ""
    for name in array:
        out += name + " & "
    return out

if __name__ == "__main__":
    app.run(debug=True)
