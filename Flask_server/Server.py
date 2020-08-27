# Importing flask module in the project is mandatory 
# An object of Flask class is our WSGI application. 
from flask import Flask ,jsonify
from flask_cors import CORS, cross_origin
# from flask_pymongo import PyMongo
from flask_pymongo import pymongo
from flask import request
import json

app = Flask(__name__)
CORS(app)

CONNECTION_STRING="mongodb+srv://Vd4vennam:Vd4vennam@cluster0.ulcey.mongodb.net/TradeTech?retryWrites=true&w=majority"
# mongo = PyMongo(app, uri=)
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('TradeTech')
AlterData_collection = pymongo.collection.Collection(db, 'userDetails')

# Flask constructor takes the name of 
# current module (__name__) as argument. 
# app = Flask(__name__) 

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function. 
@app.route('/') 
# ‘/’ URL is bound with hello_world() function. 
def hello_world():
	return 'Hello World'


@app.route('/getDetails') 
# ‘/’ URL is bound with hello_world() function. 
def details(): 
	return jsonify({'status':200,'message':'The message from flask server'})

@app.route('/check')
def check():
    # username = request.args.get('username')
    AlterData_collection.insert_one({"name": "vennam","username":'Dev567'})
    # user = db.AlterData.find_one_or_404({"_id": username})
    return 'The Data Hase been uploaded Sucessfully '

@app.route("/signin/")
def signin():
    username = request.args.get('username')
    user = AlterData_collection.find_one({"username": username})
    return json.dumps(user, default=str)

# main driver function 
if __name__ == '__main__': 

	# run() method of Flask class runs the application 
	# on the local development server. 
	app.run(debug=True) 
