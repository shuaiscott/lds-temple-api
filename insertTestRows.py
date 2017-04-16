from pymongo import MongoClient

client = MongoClient('mongodb://scott:tootles@ds161410.mlab.com:61410/lds-temples-api')
db = client['lds-temples-api']
col_temples = db['temples']
col_sessions = db['sessions']

payson = { 'id' : 'payson-utah',
    'name' : 'Payson Utah Temple' }

id = col_temples.insert_one(payson).inserted_id
print id