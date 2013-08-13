import couchdb
import json

def add_entry(db, uuid, entry):
    doc = {"uuid": uuid, "data": entry}
    doc_id = db.save(doc)

def get_entries(db, uuid):
    print "Entries for user: ", uuid
    entries = []
    for row in db.view('entries/get_entries'):
        if row.key == uuid:
            entries.append(row.value)
            #print row.key, json.dumps(row.value['data'])
    return entries


def get_entry_list(db, uuid):
    print "Entry list for user: ", uuid
    entrylist = []
    idx = 1
    for row in db.view('entries/get_entries'):
        if row.key == uuid:

            entrylist.append( {"id": idx, "date": row.value['data']['date']})
            idx = idx + 1
    return entrylist

