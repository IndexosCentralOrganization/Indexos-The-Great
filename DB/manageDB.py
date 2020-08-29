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
def existeItem(table, primKey_name, primKey_var):
    """
    table -> str : Nom de la table
    primKey_name -> str : Nom de la clef primaire
    primKey_var -> str|int : Valeur de la clef primaire a tester
    """
    cursor = conn.cursor()
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

# def addItem(table, listDict):
#     """
#     table -> str : Nom de la table
#     listDict -> dict : dictionnaire formatté {param0:value0, param1:value1}
#     """
#     i = 0
#     cursor = conn.cursor()
#     req = "INSERT INTO {0}".format(table) + '('
#     for item in listDict:
#         if i == 0:
#             req += item
#         else:
#             req += ','+item
#         i =+ 1
#     req += ') VALUES ('
#
#     i = 0
#
#     for item in listDict:
#         if i == 0:
#             req += listDict[item]
#         else:
#             req += ',' + listDict[item]
#         i =+ 1
#
#     req =+ ')'
#
#     cursor.execute(req)


# Commandes sur les auteurs
def addAuteur(authid):
    if existAuteur(authid) is False:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO auteur (id) VALUES (?)", (authid,))

        return False
    else:
        return True


def deleteAuteur(authid):
    return deleteItem("auteur", "id", authid)


def existAuteur(authid):
    return existeItem("auteur", "id", authid)


# Commande sur les liens
def addLien():
    pass


def deleteLien(url):
    return deleteItem("lien", "URL", url)


def existLien(url):
    return existeItem("lien", "URL", url)


# Commandes sur les tag
def addTag():
    pass


def deleteTag(id):
    return deleteItem("tag", "id", id)


def existTag(id):
    return existeItem("tag", "id", id)


# Commande sur la tagmap
def addTagmap():
    pass


def deleteTagmap(id):
    return deleteItem("tagmap", "id", id)


def existTagmap(id):
    return existeItem("tagmap", "id", id)


# Commandes sur les events
def addEvent():
    pass


def deleteEvent(id):
    return existeItem("event", "id", id)


def existEvent(id):
    return existeItem("event", "id", id)

# Commandes sur les synonymes
def addSynonyme():
    pass


def deleteSynonyme(old):
    return existeItem("synonyme", "old", old)


def existSynonyme(old):
    return existeItem("synonyme", "old", old)


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


def deleteSyn(oldSyn, authID):
    """
    Supprime le synonyme qui correspond a old si les authID sont égal
    """
    cursor = conn.cursor()
    cursor.execute("SELECT authID FROM synonyme where old == ?", (oldSyn,))
    authfdb = cursor.fetchone()
    if authfdb is not None:
        if int(authID) == int(authfdb[0]):
            cursor.execute("DELETE FROM synonyme WHERE old == ?", (oldSyn,))
            conn.commit()

            return True
        else:
            return False
    else:
        return False


def tagtotags(tag):
    return (" chanName ='{}' OR tag1 = '{}' OR tag2 = '{}' OR tag3 = '{}'".format(tag, tag, tag, tag))


def search(tagtuple):
    """
    Recherche les tags du tuple selon les règles boolennes
    """
    n = 0
    for item in tagtuple:
        if item != "||" and item != "&&" and item != "^" and item != "!":
            tagtuple = tagtuple[:n] + ('('+tagtotags(item)+')', ) + tagtuple[n+1:]
        elif item == '||':
            tagtuple = tagtuple[:n] + ("OR", ) + tagtuple[n+1:]
        elif item == '&&':
            tagtuple = tagtuple[:n] + ("AND", ) + tagtuple[n+1:]
        elif item == '^':
            tagtuple = tagtuple[:n] + ("XOR", ) + tagtuple[n+1:]
        elif item == '!':
            tagtuple = tagtuple[:n] + ("NOT", ) + tagtuple[n+1:]
        n += 1

    cond_req = ""
    for item in tagtuple:
        cond_req += ' '+item+' '

    cursor = conn.cursor()
    req = "SELECT * FROM link WHERE " + cond_req
    print(req)
    cursor.execute(req)
    return cursor.fetchall()


def searchByTag(tag):
    """
    Recherche des liens en fonction d'un tag
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM link WHERE tag1 == ? OR tag2 == ? OR tag3 == ?", (tag, tag, tag))
    return cursor.fetchall()


def searchByChan(chanName):
    """
    Recherche des liens en fonction du nom du channel
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM link WHERE chanName == ?", (chanName,))
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


def allSynonyme():
    """
    Permet de récupérer tous les synonymes
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM synonyme")
    res = cursor.fetchall()
    return res




# conn.close()
