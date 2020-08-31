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


# Utils
def dumpAllDB():
    """
    Dump toute la base de donnée dans dump.sql
    """
    name = 'dump.sql'
    with open(name, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    return name


def existeItem(table, primKey_name, primKey_var):
    """
    table -> str : Nom de la table
    primKey_name -> str : Nom de la clef primaire
    primKey_var -> str|int : Valeur de la clef primaire a tester
    """
    cursor = conn.cursor()
    if isinstance(primKey_var, str):
        req = "SELECT * FROM {0} WHERE {1} like \"{2}\"".format(table, primKey_name, primKey_var)
    else:
        req = "SELECT * FROM {0} WHERE {1} == {2}".format(table, primKey_name, primKey_var)

    cursor.execute(req)
    ret = len(cursor.fetchall())

    if ret > 0:
        return True
    else:
        return False


def deleteItem(table, primKey_name, primKey_var):
    """
    table -> str : Nom de la table
    primKey_name -> str : Nom de la clef primaire
    primKey_var -> str|int : Valeur de la clef primaire a tester
    """
    if existeItem(table, primKey_name, primKey_var) is False:
        return False

    cursor = conn.cursor()
    req = "DELETE FROM {0} WHERE {1} == {2}".format(table, primKey_name, primKey_var)
    cursor.execute(req)
    conn.commit()
    ret = existeItem(table, primKey_name, primKey_var)

    if ret:
        return False
    else:
        return True


def allItem(table):
    """
    table -> str : Nom de la table dont on veux toutes les lignes
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM {0}".format(table))
    res = cursor.fetchall()
    return res


def simpleItemSearch(table, col_name, col_val):
    cursor = conn.cursor()
    if isinstance(col_val, str):
        cursor.execute("SELECT * FROM {0} WHERE {1} LIKE {2}".format(table, col_name, col_val))
    else:
        cursor.execute("SELECT * FROM {0} WHERE {1} == {2}".format(table, col_name, col_val))

    res = cursor.fetchall()
    return res


# Commandes sur les auteurs
def addAuteur(authid):
    if existAuteur(authid) is False:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO auteur (id) VALUES (?)", (authid,))
        conn.commit()
        return True
    else:
        return False


def deleteAuteur(authid):
    return deleteItem("auteur", "id", authid)


def existAuteur(authid):
    return existeItem("auteur", "id", authid)


def allAuteur():
    return allItem("auteur")


def searchAuteurByPrimKey(primkey):
    return simpleItemSearch("auteur", "id", primkey)

# Commande sur les liens
def addLien(url, chanName, langue, authid):
    if existLien(url) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO lien (url, chanName, langue, authid) VALUES (\"{0}\", \"{1}\", \"{2}\", {3})".format(url, chanName, langue, authid)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteLien(url):
    return deleteItem("lien", "URL", url)


def existLien(url):
    return existeItem("lien", "URL", url)


def allLien():
    return allItem("lien")


def searchLienByPrimKey(primkey):
    return simpleItemSearch("lien", "URL", primkey)


# Commandes sur les tag
def addTag(value, id, description, authid):
    if existTag(id) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO lien (value, description, authid) VALUES (\"{0}\", \"{1}\", {2})".format(value, description, authid)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteTag(id):
    return deleteItem("tag", "id", id)


def existTag(id):
    return existeItem("tag", "id", id)


def allTag():
    return allItem("tag")


def searchTagByPrimKey(primkey):
    return simpleItemSearch("tag", "id", primkey)


# Commande sur la tagmap
def addTagmap(id, lien_url, tag_id):
    if existTagmap(id) is False and existLien(lien_url) and existTag(tag_id):
        cursor = conn.cursor()
        req = "INSERT INTO tagmap (lien_url, tag_id) VALUES (\"{0}\", {1})".format(lien_url, tag_id)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteTagmap(id):
    return deleteItem("tagmap", "id", id)


def existTagmap(id):
    return existeItem("tagmap", "id", id)


def allTagmap():
    return allItem("tagmap")


def searchTagmapByPrimKey(primkey):
    return simpleItemSearch("tagmap", "id", primkey)


# Commandes sur les events
def addEvent(id, url, begin_date, end_date, authid):
    if existEvent(id) is False and existLien(url):
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO event (url, begin_date, end_date, authid) VALUES (\"{0}\", \"{1}\", \"{2}\", {3})".format(url, begin_date, end_date, authid)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteEvent(id):
    return existeItem("event", "id", id)


def existEvent(id):
    return existeItem("event", "id", id)


def allEvent():
    return allItem("event")


def searchEventByPrimKey(primkey):
    return simpleItemSearch("event", "id", primkey)


# Commandes sur les synonymes
def addSynonyme(authid, old, new):
    if existSynonyme(old) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO synonyme (authid, old, new) VALUES ({0}, \"{1}\", \"{2}\")".format(authid, old, new)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteSynonyme(old):
    return existeItem("synonyme", "old", old)


def existSynonyme(old):
    return existeItem("synonyme", "old", old)


def allSynonyme():
    return allItem("synonyme")


def searchSynonymeByPrimKey(primkey):
    return simpleItemSearch("synonyme", "old", primkey)


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
