import couchdb

from couchdb.http import PreconditionFailed, ResourceNotFound, ResourceConflict

def init_db(name, url):
    """
    Check whether the database 'name' exists on the couchdb server at url. If so, return reference to the server object. Otherwise create a new DB called name at url then return the new server object.
    
    Return: A CouchDB database object
    """   
    global db
    server = couchdb.client.Server(url)

    try: 
        db = server.create(name)
    except PreconditionFailed:
        db = server[name]
    except:
        print "Failed to connect to the SUPERHUB users database. Is the CouchDB server running?"
        exit(1)
    return db
