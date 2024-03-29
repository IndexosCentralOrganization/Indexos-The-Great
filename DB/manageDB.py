import sqlite3 as sql
import json
import os

path = os.path.realpath(__file__).replace(__name__.split('.')[1]+'.py', "")
conn = sql.connect(path+'/dataBase.db')


def initDB():
    with open(path+'/create_intruct.json') as json_file:
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
    name = path+'/dump.sql'
    with open(name, 'w') as f:
        for line in conn.iterdump():
            f.write('%s\n' % line)
    return name


def colOccurence(colName, tableName):
    """
    colName -> Nom de la colonne dont ont veux le nombre d'occurence en fonction du
               nombre de lien
    tableName -> Nom de la table
    """
    cursor = conn.cursor()
    req = "SELECT {0}, COUNT(*) FROM {1} GROUP BY {0}".format(colName, tableName)
    cursor.execute(req)
    return cursor.fetchall()


def updateItem(table, primKey_name, primKey_var, keyName, keyVal):
    """
    table -> nom de la table
    primKey_name -> Nom de la clef primaire
    primKey_var -> valeur de la clef primaire
    keyName -> nom de la clef a changer
    keyVal -> valeur de la clef a changer
    """

    cursor = conn.cursor()
    if isinstance(keyVal, str):
        req = "UPDATE {0} SET {1} = \'{2}\' ".format(table, keyName, keyVal)
    else:
        req = "UPDATE {0} SET {1} = {2} ".format(table, keyName, keyVal)

    if isinstance(primKey_var, str):
        req += "WHERE {0} LIKE \'{1}\'".format(primKey_name, primKey_var)
    else:
        req += "WHERE {0} == {1}".format(primKey_name, primKey_var)

    cursor.execute(req)
    conn.commit()


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
    if isinstance(primKey_var, str):
        req = "DELETE FROM {0} WHERE {1} LIKE \"{2}\"".format(table, primKey_name, primKey_var)
    else:
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
        cursor.execute("SELECT * FROM {0} WHERE {1} LIKE \"{2}\"".format(table, col_name, col_val))
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
def addLien(url, chanName, langue, authid, preview_title, preview_desc):
    if existLien(url) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO lien (url, chanName, langue, authid, preview_title, preview_desc) VALUES (\"{0}\", \"{1}\", \"{2}\", {3}, \"{4}\", \"{5}\")".format(url, chanName, langue, authid, preview_title, preview_desc)
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
def addTag(value, description, authid):
    if existTag(value) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO tag (value, description, authid) VALUES (\"{0}\", \"{1}\", {2})".format(value, description, authid)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteTag(value):
    return deleteItem("tag", "value", value)


def existTag(value):
    return existeItem("tag", "value", value)


def allTag():
    return allItem("tag")


def searchTagByPrimKey(primkey):
    return simpleItemSearch("tag", "value", primkey)


# Commande sur la tagmap
def addTagmap(lien_url, tag_value):
    if existTagmap(lien_url, tag_value) is False and existLien(lien_url) and existTag(tag_value):
        cursor = conn.cursor()
        req = "INSERT INTO tagmap (lien_url, tag_value) VALUES (\"{0}\", \"{1}\")".format(lien_url, tag_value)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteTagmap(id):
    return deleteItem("tagmap", "id", id)


def existTagmap(lien_url, tag_value):
    cursor = conn.cursor()
    req = "SELECT * FROM tagmap WHERE lien_url like \"{0}\" AND tag_value like \"{1}\"".format(lien_url, tag_value)

    cursor.execute(req)
    ret = len(cursor.fetchall())

    if ret > 0:
        return True
    else:
        return False


def allTagmap():
    return allItem("tagmap")


def searchTagmapByPrimKey(primkey):
    return simpleItemSearch("tagmap", "id", primkey)


# Commandes sur les events
def addEvent(url, begin_date, end_date, authid):
    if existLien(url) is True and existEvent(url) is False:
        addAuteur(authid)
        cursor = conn.cursor()
        req = "INSERT INTO event (url, begin_date, end_date, authid) VALUES (\"{0}\", \"{1}\", \"{2}\", {3})".format(url, begin_date, end_date, authid)
        cursor.execute(req)
        conn.commit()

        return True
    else:
        return False


def deleteEvent(id):
    return deleteItem("event", "id", id)


def existEvent(url):
    return existeItem("event", "url", url)


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
    return deleteItem("synonyme", "old", old)


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


def searchLinkFromTags(tagtuple, lien=True):
    """
    Recherche les tags du tuple selon les règles boolennes
    retourne liste lien sans les liens présent aussi dans la table event
    """

    cursor = conn.cursor()
    req = ""
    # req = ""
    entete = "SELECT lien_url FROM tagmap "
    n = 0

    # Lsearch gris or blanc and markdown

    for item in tagtuple:
        if item == "and" or item == "AND":
            req += "\n INTERSECT \n"
        elif item == "or" or item == "OR":
            req += "\n UNION \n"
        elif item == "not" or item == "NOT":
            req += "\n EXCEPT \n"
        else:
            # On est dans le cas où c'est pas un opérateur
            req += entete
            req += "WHERE tag_value LIKE '{0}'".format(item)
    if lien:
        req += "\n EXCEPT \n SELECT url FROM event"
    else:
        req += "\n INTERSECT \n SELECT url FROM event"

    print(req)
    cursor.execute(req)
    return cursor.fetchall()

# conn.close()
