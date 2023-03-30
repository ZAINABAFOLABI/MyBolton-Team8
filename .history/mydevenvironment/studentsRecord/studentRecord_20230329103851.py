# importing Flask class flask library
from flask import Flask

# creation of  an instance of the Flask class and assign to app
# __name__ refers to the default path of the package
app = Flask(__name__)
def hello_world():
    return " <div> <h1> My Bolton</h1> <p>Team 8!</p></div>"

