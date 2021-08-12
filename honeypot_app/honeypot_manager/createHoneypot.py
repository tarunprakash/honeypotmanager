"""
Create honeypot instances from config
"""
import os
import sys

from django import db
## required to import local files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

import json
import sqlite3
from twisted.application import service
from honeypotFactory import HoneypotFactory

conn = sqlite3.connect(os.path.join(BASE_DIR, '../../db.sqlite3'))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

CONFIG_FILEPATH = os.path.join(BASE_DIR, 'honeypot.conf')

application = service.Application("opencanaryd")
factory = HoneypotFactory(application)

def getConfig():
    """Returns JSON of config file contents"""
    with open(CONFIG_FILEPATH) as file:
        return json.load(file)

def clearConfig():
    """Clear config file"""
    with open(CONFIG_FILEPATH, 'w') as file:
        json.dump({
            "honeypotIP": "",
            "honeypotType": ""
        }, file)

def getDbEntries():
    """Returns all DB entries"""
    query = "SELECT * FROM honeypot_app_honeypot;"
    return cursor.execute(query).fetchall()

def ipExistsDb(ip):
    """Check if IP exists in DB"""
    query = f'SELECT EXISTS(SELECT 1 FROM honeypot_app_honeypot WHERE honeypotIP="{ip}");'

def createHoneypot():
    """Creates honeypot from config info"""
    config = getConfig()
    
    dbEntries = getDbEntries()
    honeypotIPs, honeypotTypes = [], []
    for row in dbEntries:
        honeypotIPs.append(row['honeypotIP'])
        honeypotTypes.append(row['honeypotType'])

    ## config not in db (stale config)
    if config['honeypotIP'] not in honeypotIPs \
        or config['honeypotType'] not in honeypotTypes:
        print('STALE CONFIG')
        clearConfig()
        return

    factory.addHoneypot(config['honeypotType'], config['honeypotIP'])

    return

createHoneypot()
