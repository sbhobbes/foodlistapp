from socket import create_connection
import sqlite3
from sqlite3 import Error


# People table scripts
def InsertNewPerson(db, first, middle, last):

    # SQL to create a new People record
    sql = '''INSERT INTO
                PEOPLE (FIRST_NAME, MIDDLE_INITIAL, LAST_NAME)
             VALUES
                (?, ?, ?)'''

    # Execute the SQL
    list = (first, middle, last)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)

def UpdatePerson(db, id, first, middle, last):

    # SQL to update a record in the People table
    sql = """UPDATE 
                PEOPLE
             SET
                FIRST_NAME = ?,
                MIDDLE_NAME = ?,
                LAST_NAME = ?
             WHERE
                PERSON_ID = ?;"""
    
    list = (first, middle, last, id)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)
    UpdateActivityLog()


# List Header table scripts
def InsertNewListHeader(db, listName, firstName, lastName):
    
    # SQL to create a new List Header record
    sql = '''INSERT INTO
                LIST_HEADERS (DESCRIPTION, PERSON_ID)
             VALUES
                (?, (SELECT PERSON_ID FROM PEOPLE WHERE FIRST_NAME = ? AND LAST_NAME = ?))'''
    
    # Execute the SQL
    list = (listName, firstName, lastName)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# List Lines table scripts
def InsertNewListLine(db, header, itemID, date):

    # SQL to create a new List Line record
    sql = '''INSERT INTO
                LIST_LINES (HEADER_ID, ITEM_ID, DAY_DT)
             VALUES
                (?, ?, ?);'''

    # Execute the SQL
    list = (header, itemID, date)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# Item table scripts
def InsertNewItem(db, description):

    # SQL to create a new Item record
    sql = '''INSERT INTO
                ITEMS (DESCRIPTION)
             VALUES
                (?)'''

    print(description)
    
    # Execute the SQL
    list = [(description)]
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# Reaction table scripts
def InsertNewReaction(db, firstName, lastName, date):

    # SQL to create a new Reaction record
    sql = '''INSERT INTO
                REACTIONS (PERSON_ID, DAY_DT)
             VALUES
                ((SELECT PERSON_ID FROM PEOPLE WHERE FIRST_NAME = ? AND LAST_NAME = ?), ?)'''

    # Execute the SQL
    list = (firstName, lastName, date)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# Lookups table scripts
def InsertNewLookups(db, description):

    # SQL to create a new Lookup record
    sql = '''INSERT INTO
                LOOKUPS (DESCRIPTION)
             VALUES
                (?);'''

    # Execute the SQL
    list = [(description)]
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


def InsertNewListHeader(db, personID, description):
    
    # SQL to insert a new list header record
    sql = '''INSERT INTO
                LIST_HEADERS (DESCRIPTION, PERSON_ID)
             VALUES
                (?, ?);'''

    list = [description, personID]
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# Retrieve a list of full names from the people table
def SelectPeople(db):
    
    # SQL to get list of people
    sql = '''SELECT
                PERSON_ID,
                FULL_NAME
             FROM
                PEOPLE
             ORDER BY
                FULL_NAME ASC'''

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    peopleList = []
    rows = c.fetchall()
    for row in rows:
        peopleList.append((row[0], row[1]))

    conn.close()

    return peopleList


# Retrieve a list of items from the item table
def SelectItems(db):

    # SQL to get list of items
    sql = '''SELECT 
                ITEM_ID,
                DESCRIPTION
             FROM
                ITEMS
             ORDER BY
                DESCRIPTION ASC'''

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    itemList = []
    rows = c.fetchall()
    for row in rows:
        itemList.append((row[0], row[1]))

    conn.close()

    return itemList


def SelectListHeaders(db):

    # SQL to get list of list headers
    sql = '''SELECT
                HEADER_ID,
                DESCRIPTION
             FROM
                LIST_HEADERS
             ORDER BY
                DESCRIPTION ASC;'''

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    listHeadersList = []
    rows = c.fetchall()
    for row in rows:
        listHeadersList.append((row[0], row[1]))

    conn.close()
    
    return listHeadersList


def SelectHistory(db, fromDate, toDate):

    # SQL to retrieve values from the history view
    sql = '''SELECT
                LL.DAY_DT,
                I.DESCRIPTION
             FROM
                LIST_LINES LL,
                ITEMS I
             WHERE I.ITEM_ID = LL.ITEM_ID'''
             #WHERE
                #DATE(DAY_DT) BETWEEN %s AND %s;''' % (fromDate, toDate)
    print(sql)

    list = [fromDate, toDate]

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    historyView = []
    rows = c.fetchall()
    for row in rows:
        historyView.append(row)
    print(rows)
    conn.close()

    return historyView


# 
def SelectTableNames(db):
    
    # SQL to retrieve table names
    sql = '''SELECT
                TABLE_NAME
             FROM
                ALL_TABLES 
             WHERE
                NOT TABLE_NAME IN ('sqlite_sequence', 'ACTIVITY_LOG') 
             ORDER BY 
                TABLE_NAME ASC;'''

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    tableData = []
    rows = c.fetchall()
    for row in rows:
        tableData.append(row)

    conn.close()

    return tableData


def SelectEntireTable(db, tableName):
    
    # SQL to retrieve all data from the desired table
    sql = '''SELECT
                *
             FROM
                %s''' % (tableName)

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)

    tableData = []
    rows = c.fetchall()
    for row in rows:
        tableData.append(row)

    conn.close()

    return tableData


def DeleteFromTable(db, tableName, columnName, matchValue):

    # SQL to delete a record from a table
    sql = '''DELETE FROM
                %s
             WHERE
                %s = %s;
                ''' %(tableName, columnName, matchValue)

    conn = CreateConnection(db)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()
    conn.close()


# Database connection and query execution logic
def CreateConnection(db):

    # Create connection object as None type
    conn = None

    # Create the connection from the DB file parameter
    try:
        conn = sqlite3.connect(db)
        print(sqlite3.version)
    except Error as e:      # Handle exceptions
        print(e)
    
    # Return the connection object to the calling function
    return conn


# Execute a query against the database
def ExecuteQuery(conn, sql, list):
    """This function is designed to execute a SQL statement against a
    SQLite database.
        :param conn: a database connection object
        :param sql: a valid SQL statement with question marks denoting variables in the statement
        :param list: a list of values which will be used to replace the question marks in the order
        in which they appear within the SQL statement."""

    # Check if a connection exists, execute the query, and then close the connection
    if conn:
        c = conn.cursor()
        c.execute(sql, list)
        conn.commit()
        conn.close()