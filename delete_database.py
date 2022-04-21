import sqlite3
from sqlite3 import Error

def main():

    deletePeople = '''DELETE FROM PEOPLE;'''
    dropPeopleTable = '''DROP TABLE IF EXISTS PEOPLE;'''
    deleteUsers = '''DELETE FROM USERS;'''
    dropUsersTable = '''DROP TABLE IF EXISTS USERS;'''
    deleteListHeaders = '''DELETE FROM LIST_HEADERS'''
    dropListHeadersTable = '''DROP TABLE IF EXISTS LIST_HEADERS;'''
    deleteItems = '''DELETE FROM ITEMS;'''
    dropItemsTable = '''DROP TABLE IF EXISTS ITEMS;'''
    deleteListLines = '''DELETE FROM LIST_LINES;'''
    dropListLinesTable = '''DROP TABLE IF EXISTS LIST_LINES;'''
    deleteReactions = '''DELETE FROM REACTIONS;'''
    dropReactionsTable = '''DROP TABLE IF EXISTS REACTIONS;'''

    deleteList = [deleteUsers, deletePeople, deleteListHeaders, deleteItems,
                    deleteListLines, deleteReactions]
    dropTablesList = [dropPeopleTable, dropUsersTable, dropListHeadersTable,
                        dropItemsTable, dropListLinesTable, dropReactionsTable]

    conn = None

    try:
        conn = sqlite3.connect(r'db/foodtracker.db')
        c = conn.cursor()

        for table in deleteList:
            c.execute(table)

        for table in dropTablesList:
            c.execute(table)
        
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()