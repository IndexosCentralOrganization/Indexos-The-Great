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


def addLink(link, tag1=None, tag2=None, tag3=None):
    """
    link -> string
    tag1 -> string
    tag2 -> string
    tag3 -> string
    """
    cursor = conn.cursor()

    if tag1:
        cursor.execute("INSERT INTO link (`URL`,`tag1`) VALUES (?, ?)", (link, tag1))

    elif tag2:
        cursor.execute("INSERT INTO link (`URL`,`tag1`, `tag2`) VALUES (?, ?, ?)", (link, tag1, tag2))

    elif tag3:
        cursor.execute("INSERT INTO link (`URL`,`tag1`, `tag2`, `tag3`) VALUES (?, ?, ?, ?)", (link, tag1, tag2, tag3))

    else:
        cursor.execute("INSERT INTO link (`URL`) VALUES (?)", link)
    conn.commit()
