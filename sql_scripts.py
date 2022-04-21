import sqlite3
from sqlite3 import Error

def InsertNewPerson(db, first, middle, last):

    sql = '''INSERT INTO
                PEOPLE (FIRST_NAME, MIDDLE_INITIAL, LAST_NAME)
             VALUES
                (?, ?, ?)'''

    list = (first, middle, last)
    print(list)

    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)

def InsertNewListHeader(db, listName, firstName, lastName):
    
    sql = '''INSERT INTO
                LIST_HEADERS (DESCRIPTION, PERSON_ID)
             VALUES
                (?, (SELECT PERSON_ID FROM PEOPLE WHERE FIRST_NAME = ? AND LAST_NAME = ?))'''
    
    list = (listName, firstName, lastName)

    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)

def InsertNewItem(db, description):

    sql = '''INSERT INTO
                ITEMS (DESCRIPTION)
             VALUES
                (?)'''
    
    list = [(description)]
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)

def InsertNewReaction(db, firstName, lastName, date):

    sql = '''INSERT INTO
                REACTIONS (PERSON_ID, DAY_DT)
             VALUES
                ((SELECT PERSON_ID FROM PEOPLE WHERE FIRST_NAME = ? AND LAST_NAME = ?), ?)'''

    list = (firstName, lastName, date)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)

def CreateConnection(db):

    conn = None

    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as e:
        print(e)
    
    return conn

def ExecuteQuery(conn, sql, list):

    if conn:
        c = conn.cursor()
        c.execute(sql, list)
        conn.commit()
        conn.close()