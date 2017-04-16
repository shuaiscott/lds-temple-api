from bs4 import BeautifulSoup
import requests
import re
import config
from pymongo import MongoClient

client = MongoClient('mongodb://' + config.db_user_admin + ':' + config.db_password_admin + '@ds161410.mlab.com:61410/lds-temples-api')
db = client['lds-temples-api']
col_temples = db['temples']

temples = []

# extract temple list of names and ids
source = requests.get("https://www.lds.org/church/temples/find-a-temple?lang=eng").text
soup = BeautifulSoup(source, "html5lib")
table = soup.find("tbody", {"id": "temple-list-sortable"})
for row in table.find_all('tr'):
    name_href = row.find_all('td')[0]
    href = name_href.a['href']
    id = re.search('https:\/\/www.lds.org\/church\/temples\/([\w-]*)\?', href).group(1)
    name = name_href.a.string
    dedication_date = row.find_all('td')[2].string
    # add to temple list
    temple = { '_id': id, 'name': name, 'dedication_date': dedication_date, 'href': href }
    temples.append(temple)
    # add to MongoDB
    db_id = col_temples.update({'_id': id}, temple, upsert=True )
    print 'Inserted ' + id
