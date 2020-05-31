import sqlite3 as sql
import json

conn = sql.connect('DB/dataBase.db')


def initDB():
    with open('DB/create_intruct.json') as json_file:
        cr_in = json.load(json_file)
    for i in cr_in:
        cursor = conn.cursor()
        script = cr_in[i]
        cursor.execute(script)
        conn.commit()
    return True


def addLink(link,authID, chanName, tag1=None, tag2=None, tag3=None):
    """
    link -> string
    tag1 -> string
    tag2 -> string
    tag3 -> string
    """
    cursor = conn.cursor()

    if tag3:
        cursor.execute("INSERT INTO link (URL,authID,chanName,tag1, tag2, tag3) VALUES (?, ?, ?, ?, ?, ?)", (link, authID, chanName, tag1, tag2, tag3))

    elif tag2:
        cursor.execute("INSERT INTO link (URL, authID,chanName,tag1, tag2) VALUES (?, ?, ?, ?, ?)", (link, authID, chanName, tag1, tag2))

    elif tag1:
        cursor.execute("INSERT INTO link (URL, authID,chanName,tag1) VALUES (?, ?, ?, ?)", (link, authID, chanName, tag1))

    else:
        cursor.execute("INSERT INTO link (URL, authID,chanName) VALUES (?, ?, ?)", (link, authID, chanName))
    conn.commit()


def deleteLink(link, authID):
    """
    Supprime le lien qui correspond a link si les authID sont égal
    """
    cursor = conn.cursor()
    print(link)
    print(authID)
    cursor.execute("SELECT authID FROM link where URL == ?", (link,))
    authfdb = cursor.fetchone()
    print(authfdb)
    if authfdb is not None:
        if int(authID) == int(authfdb[0]):
            cursor.execute("DELETE FROM link WHERE URL == ?", (link,))
            conn.commit()

            return True
        else:
            return False
    else:
        return False

def searchID():
    pass
# conn.close()
