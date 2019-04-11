from flask import Flask
from flask import request
from flask_cors import CORS
from flask_pymongo import PyMongo
import urllib
import json
import os
import sys
import time
import email_service

app = Flask(__name__)
CORS(app)

db_host = os.getenv('DB_HOST', 'localhost')
db_port = os.getenv('DB_PORT', '27017')

db_user = os.getenv('DB_USER', 'sumo')
db_password = os.getenv('DB_PASS', 'password')

app.config['MONGO_URI'] = "mongodb://{}:{}@{}:{}/pandas?authSource=admin".format(db_user, urllib.parse.quote(db_password), db_host, db_port)
mongo = PyMongo(app)

print("---------------------")
print("Testing db connection ...")
print(mongo.cx.server_info())
print("Testing email service ...")

try:
    email_service.preflight_check()
except RuntimeWarning as e:
    print('WARNING! ' + (str(e)))
    print('Email service may not work properly')
except Exception as e:
    print(str(e))
    sys.exit(4)

print("KUDOS!")
print("---------------------")


@app.route('/')
def hello_world():
    return 'Hello, Pandas!'


@app.route('/p/<uuid>',  methods=['POST', 'GET'])
def add_or_get_panda(uuid):
    if request.method == 'POST':
        payload = request.get_json()
        print(payload)
        if payload is not None:
            mongo.db.pandas.insert({
                '_id': uuid,
                'userid': payload.get('userid'),
                'insert_ts': int(time.time()),
                'bbox': payload.get('bbox', []),
                'title': payload.get('title', ''),
                'data': payload.get('content', {})}
            )

            return 'Added %s' % uuid, 200
        return "Missing data", 400
    else:
        print("Looking up {}".format(uuid))
        panda = mongo.db.pandas.find_one_or_404({"_id": uuid})
        content = panda['data']
        if content is not None:
            return json.dumps({
                u"uuid": uuid,
                u"userid": panda.get('userid', ''),
                u"bbox": panda.get('bbox', []),
                u"title": panda.get('title', ''),
                u"content": content}), 200, {'Content-Type': 'application/json'}
        return "Not found", 400


@app.route('/lastn/<count>')
def show_last_n_pandas(count):
    if 10 >= int(count)< 0:
        limit = 10
    else:
        limit = int(count)
    rs = mongo.db.pandas.find().sort([("insert_ts", -1)]).limit(limit)
    return json.dumps(list(rs))


@app.route('/email', methods=['POST'])
def sendemail():
    payload = request.get_json()
    if payload is None:
        return "Json payload empty", 400

    uuid = payload['uuid']
    email = payload['email']
    panda = mongo.db.pandas.find_one_or_404({"_id": uuid})
    geojson = panda['data']
    if geojson is not None:
        # description = panda['description']
        status = email_service.sendmail(uuid, "", email)
        mongo.db.emails.insert({
            '_id': uuid,
            'email': email,
            'status': status,
            'insert_ts': int(time.time())}
        )
        return "OK", 200
    return "Not found", 404

