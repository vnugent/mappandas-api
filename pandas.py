from flask import Flask
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
import urllib
import json
import os


app = Flask(__name__)
CORS(app)

db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '27017')

db_user = os.getenv('DB_USER', 'pandas')
db_password = os.getenv('DB_PASS', 'password')

app.config['MONGO_URI'] = "mongodb://{}:{}@{}:{}/pandas?authSource=admin".format(db_user, urllib.parse.quote(db_password), db_host, db_port)
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/p/<uuid>',  methods=['POST', 'GET'])
def show_user_profile(uuid):
    if request.method == 'POST':
        data = request.get_json()
        if data is not None:
            mongo.db.pandas.insert({
                '_id': uuid,
                'data': data})
            return 'Added %s' % uuid, 200
        return "Missing data", 400
    else:
        print("Looking up {}".format(uuid))
        panda = mongo.db.pandas.find_one_or_404({"_id": uuid})
        geojson = panda['data']
        if geojson is not None:
            return json.dumps(geojson), 200, {'Content-Type': 'application/json'}
        return "Not found", 400


@app.route('/post/<uuid:post_uuid>')
def show_post(post_uuid):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_uuid


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath
