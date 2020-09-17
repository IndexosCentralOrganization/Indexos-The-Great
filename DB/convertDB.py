import sqlite3 as sql
import json
from os import remove as rm
from webpreview import web_preview


try:
    rm('new.db')
except:
    print("DB non supprimée")

connNEW = sql.connect('new.db')
connOLD = sql.connect('old.db')


def initDB():
    with open('create_intruct.json') as json_file:
        cr_in = json.load(json_file)
    for i in cr_in:
        cursor = connNEW.cursor()
        script = cr_in[i]
        cursor.execute(script)
        connNEW.commit()
    return True


initDB()

cursorOLD = connOLD.cursor()
cursorNEW = connNEW.cursor()
err = open("file_error.txt", 'w')
cursorOLD.execute("SELECT * FROM link")
res = cursorOLD.fetchall()

for item in res:
    try:
        cursorNEW.execute("INSERT INTO auteur (id) VALUES ({})".format(item[1]))
        connNEW.commit()
    except sql.IntegrityError:
        print("Auteur déjà existant")

    title, description = "", ""
    print("\n\n>> {}\n".format(item[0]))

    if ".pdf" not in item[0]:
        try:
            ret = web_preview(item[0], timeout=1)
            title, description = ret[0], ret[1]
            if description:
                description = description.replace("\"", "'")
        except:
            pass

    print("INSERT INTO lien (URL, chanName, langue, authid, preview_title, preview_desc) VALUES (\"{0}\", \"{1}\", \"??\", {2}, \"{3}\", \"{4}\")".format(item[0], item[2], item[1], title, description))
    try:
        cursorNEW.execute("INSERT INTO lien (URL, chanName, langue, authid, preview_title, preview_desc) VALUES (\"{0}\", \"{1}\", \"??\", {2}, \"{3}\", \"{4}\")".format(item[0], item[2], item[1], title, description))
        connNEW.commit()
    except:
        err.write("{}\n".format(item[0]))
        print("ERREUR SUR LE LIEN")

    try:
        if item[3] != None:
            cursorNEW.execute("INSERT INTO tag (value, description, authid) VALUES (\"{0}\", \"\", {1})".format(item[3], item[1]))
            connNEW.commit()
    except sql.IntegrityError:
        print("Tag déjà existant")
        cursorNEW.execute("INSERT INTO tagmap (lien_url, tag_value) VALUES (\"{0}\", \"{1}\")".format(item[0], item[3]))
        connNEW.commit()

    try:
        if item[4] != None:
            cursorNEW.execute("INSERT INTO tag (value, description, authid) VALUES (\"{0}\", \"\", {1})".format(item[4], item[1]))
            connNEW.commit()
    except sql.IntegrityError:
        print("Tag déjà existant")
        cursorNEW.execute("INSERT INTO tagmap (lien_url, tag_value) VALUES (\"{0}\", \"{1}\")".format(item[0], item[4]))
        connNEW.commit()

    try:
        if item[5] != None:
            cursorNEW.execute("INSERT INTO tag (value, description, authid) VALUES (\"{0}\", \"\", {1})".format(item[5], item[1]))
            connNEW.commit()
    except sql.IntegrityError:
        print("Tag déjà existant")
        cursorNEW.execute("INSERT INTO tagmap (lien_url, tag_value) VALUES (\"{0}\", \"{1}\")".format(item[0], item[5]))
        connNEW.commit()

connNEW.close()
connOLD.close()
