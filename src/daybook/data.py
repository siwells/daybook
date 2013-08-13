import couchdb
import json

def add_entry(db, uuid, entry):
    doc = {"uuid": uuid, "data": entry}
    doc_id = db.save(doc)
