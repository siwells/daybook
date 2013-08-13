import couchdb
import json

def add_entry(db, uuid, entry):
    print str(db), uuid, json.dumps(entry)
    print "Adding entry"
