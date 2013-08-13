import bcrypt
import couchdb
import uuid

def add_user(db, email, password, first_name, last_name):
    """
    Add a user to the specified DB using the supplied information
    
    Return the uuid (string) of the new user or None
    """
    new_uuid = str(uuid.uuid4())
    #if not exists_uuid(db, new_uuid):
    #    if not exists_email(db, email):
    salt = bcrypt.gensalt()

    pw_crypted = bcrypt.hashpw(password, salt)
    
    user_doc = { "email": email, "uuid": new_uuid, "password_hash": pw_crypted, "salt": salt, "first_name": first_name, "last_name": last_name, "verified": "false"}
    
    tmp_doc = db[new_uuid] = user_doc

    return tmp_doc['_id']
