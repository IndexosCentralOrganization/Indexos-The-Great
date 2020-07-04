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


def addLink(link, authID, chanName, tag1=None, tag2=None, tag3=None):
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
    cursor.execute("SELECT authID FROM link where URL == ?", (link,))
    authfdb = cursor.fetchone()
    if authfdb is not None:
        if int(authID) == int(authfdb[0]):
            cursor.execute("DELETE FROM link WHERE URL == ?", (link,))
            conn.commit()

            return True
        else:
            return False
    else:
        return False


def searchByTag(tag):
    """
    Recherche des liens en fonction d'un tag
    """
    cursor = conn.cursor()
    cursor.execute("SELECT URL FROM link WHERE tag1 == ? OR tag2 == ? OR tag3 == ?", (tag, tag, tag))
    return cursor.fetchall()


def searchByChan(chanName):
    """
    Recherche des liens en fonction du nom du channel
    """
    cursor = conn.cursor()
    cursor.execute("SELECT URL FROM link WHERE chanName == ?", (chanName,))
    return cursor.fetchall()


def occurenceInField(field):
    """
    Permet de savoir combien d'occrence il existe pour un champ
    """
    req = "SELECT {}, count(*) FROM link GROUP BY {};".format(field, field)
    cursor = conn.cursor()
    cursor.execute(req)
    res = cursor.fetchall()
    return res


def dumpAllDB():
    """
    Dump toute la base de donnée dans dump.sql
    """
    name = 'dump.sql'
    with open(name, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    return name


def changetags(old, new):
    """
    Change les tags == old avec new
    """
    tags = ["tag1", "tag2", "tag3"]

    for tag_name in tags:
        req = "UPDATE link SET {} = ? WHERE {} = ?".format(tag_name, tag_name)
        cursor = conn.cursor()
        print(req)
        cursor.execute(req, (new, old))


def createSynonyme(authID, old, new):
    """
    Permet de créer un nouveau synonyme dans la table du même nom
    """
    cursor = conn.cursor()
    cursor.execute("INSERT INTO synonyme (authID, old, new) VALUES (?, ?, ?)", (authID, old, new))
    conn.commit()

def synonymeConvert(old):
    """
    Permet de récupérer le synonyme de old dans la table "synonyme", si aucun existe il renvoit -1
    """
    cursor = conn.cursor()
    cursor.execute("SELECT new FROM synonyme WHERE old = ?", (old,))
    res = cursor.fetchall()
    if res != []:
        return res
    else:
        return -1

# conn.close()
