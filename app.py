import json
import os
import subprocess
import config
from bottle import route, run, Bottle, request, static_file, error, response
from pymongo import MongoClient

client = MongoClient('mongodb://' + config.db_user + ':' + config.db_password + 'ldstempleapi@ds161410.mlab.com:61410/lds-temples-api')
db = client['lds-temples-api']
col_temples = db['temples']
col_sessions = db['sessions']

app = Bottle()

@app.route('/')
def dl_queue_list():
    return static_file('index.html', root='./')

@app.route('/static/:filename#.*#')
def server_static(filename):
    return static_file(filename, root='./static')

@app.route('/temples', method='GET')
def get_temples():
    temples = []
    for temple in col_temples.find({}, {'_id': False}).sort("name"):
        temples.append(temple)
    return { 'success' : True, 'temples' : temples }

@app.route('/temples/<id>', method='GET')
def get_temple_by_id(id):
    temple = col_temples.find_one({"id": id})
    
    if temple != None:
        return { 'success' : True }
    else:
        response.status = 404

@app.route('/temples/<id>/sessions', method='GET')
def get_sessions_by_temple_id(id):
    return 'Not Implemented'
    
@app.route('/temples/<id>/sessions/next', method='GET')
def get_next_session_by_temple_id(id):
    return 'Not Implemented'
    
app.run(host='0.0.0.0', port=8080, debug=True)