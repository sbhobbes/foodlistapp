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
def InsertNewListLine(db, header, item, date):

    # SQL to create a new List Line record
    sql = '''INSERT INTO
                LIST_LINES (HEADER_ID, ITEM_ID, DAY_DT)
             VALUES
                (?, ?, ?);'''

    # Execute the SQL
    list = (header, item, date)
    conn = CreateConnection(db)
    ExecuteQuery(conn, sql, list)


# Item table scripts
def InsertNewItem(db, description):

    # SQL to create a new Item record
    sql = '''INSERT INTO
                ITEMS (DESCRIPTION)
             VALUES
                (?)'''
    
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
