import sqlite3
from sqlite3 import Error

def main():

    createPeopleTable = '''CREATE TABLE IF NOT EXISTS PEOPLE (
                            PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                            FIRST_NAME VARCHAR(40),
                            MIDDLE_INITIAL VARCHAR(1),
                            LAST_NAME VARCHAR(40),
                            FULL_NAME VARCHAR(80),
                            CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                            CREATED_DATE DATE,
                            LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
                            LAST_MODIFIED_DATE DATE
                        );'''

    createUsersTable = '''CREATE TABLE IF NOT EXISTS USERS (
                            USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                            PERSON_ID INTEGER REFERENCES PEOPLE (PERSON_ID),
                            USERNAME VARCHAR(40),
                            PASSWORD VARCHAR(40),
                            CREATED_DATE DATE,
                            LAST_MODIFIED_DATE DATE
                        );'''

    createListHeadersTable = '''CREATE TABLE IF NOT EXISTS LIST_HEADERS (
                                HEADER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                DESCRIPTION VARCHAR(40),
                                PERSON_ID INTEGER REFERENCES PEOPLE (PERSON_ID),
                                CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                                CREATED_DATE DATE,
                                LAST_MODIFIED_BY REFERENCES USERS (USER_ID),
                                LAST_MODIFIED_DATE DATE
                            );'''

    createItemsTable = '''CREATE TABLE IF NOT EXISTS ITEMS (
                            ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                            DESCRIPTION VARCHAR(40),
                            CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                            CREATED_DATE DATE,
                            LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
                            LAST_MODIFIED_DATE DATE
                        );'''

    createListLinesTable = '''CREATE TABLE IF NOT EXISTS LIST_LINES (
                                LINE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                HEADER_ID INTEGER REFERENCES LIST_HEADERS (HEADER_ID),
                                ITEM_ID INTEGER REFERENCES ITEMS (ITEM_ID),
                                DAY_DT DATE,
                                CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                                CREATED_DATE DATE,
                                LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
                                LAST_MODIFIED_DATE DATE
                            );'''

    createReactionsTable = '''CREATE TABLE IF NOT EXISTS REACTIONS (
                                REACTION_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                PERSON_ID INTEGER REFERENCES PEOPLE (PERSON_ID),
                                DAY_DT DATE,
                                DESCRIPTION VARCHAR(80),
                                LOCATION INTEGER REFERENCES LOOKUPS (LOOKUP_ID),
                                CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                                CREATED_DATE DATE,
                                LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
                                LAST_MODIFIED_DATE DATE
                            );'''

    createActivitiesTable = '''CREATE TABLE IF NOT EXISTS ACTIVITY_LOG (
                                ACTIVITY_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                TABLE_NAME VARCHAR(20),
                                RECORD_ID INTEGER,
                                PREVIOUS_VALUE VARCHAR(80),
                                NEW_VALUE VARCHAR(80),
                                CHANGED_ON_DT DATETIME
                            );'''

    createLookupsTable = '''CREATE TABLE IF NOT EXISTS LOOKUPS (
                                LOOKUP_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
                                DESCRIPTION VARCHAR(40),
                                CREATED_BY INTEGER REFERENCES USERS (USER_ID),
                                CREATED_DATE DATE,
                                LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
                                LAST_MODIFIED_DATE DATE
                            );'''

    personInsertTrigger = '''CREATE TRIGGER IF NOT EXISTS PERSON_INSERT
                                    AFTER INSERT
                                    ON PEOPLE
                                BEGIN
                                    INSERT INTO
                                        USERS (PERSON_ID, USERNAME, PASSWORD, CREATED_DATE, LAST_MODIFIED_DATE)
                                    VALUES
                                        (
                                            (SELECT PERSON_ID FROM PEOPLE WHERE PERSON_ID = NEW.PERSON_ID),
                                            (SELECT LOWER((SUBSTR(FIRST_NAME, 0, 2) || MIDDLE_INITIAL || SUBSTR(LAST_NAME, 0, 7))) FROM PEOPLE WHERE PERSON_ID = NEW.PERSON_ID),
                                            'Password1',
                                            CURRENT_DATE,
                                            CURRENT_DATE
                                        );

                                    UPDATE 
                                        PEOPLE
                                    SET
                                        FULL_NAME = FIRST_NAME || ' ' || LAST_NAME,
                                        CREATED_DATE = CURRENT_DATE,
                                        LAST_MODIFIED_DATE = CURRENT_DATE
                                    WHERE
                                        PERSON_ID = NEW.PERSON_ID;
                                END;'''

    listHeaderInertTrigger = '''CREATE TRIGGER IF NOT EXISTS LIST_HEADER_INSERT
                                    AFTER INSERT
                                    ON LIST_HEADERS
                                BEGIN
                                    UPDATE
                                        LIST_HEADERS
                                    SET
                                        CREATED_DATE = CURRENT_DATE,
                                        LAST_MODIFIED_DATE = CURRENT_DATE
                                    WHERE
                                        HEADER_ID = NEW.HEADER_ID;
                                END;'''

    listLinesInsertTrigger = '''CREATE TRIGGER IF NOT EXISTS LIST_LINES_INSERT
                                    AFTER INSERT
                                    ON LIST_LINES
                                BEGIN
                                    UPDATE
                                        LIST_LINES
                                    SET
                                        CREATED_DATE = CURRENT_DATE,
                                        LAST_MODIFIED_DATE = CURRENT_DATE;
                                END;'''

    itemInsertTrigger = '''CREATE TRIGGER IF NOT EXISTS ITEM_INSERT
                                AFTER INSERT
                                ON ITEMS
                            BEGIN
                                UPDATE
                                    ITEMS
                                SET
                                    CREATED_DATE = DATETIME(CURRENT_DATE),
                                    LAST_MODIFIED_DATE = DATETIME(CURRENT_DATE);
                            END;'''

    personUpdateTrigger = '''CREATE TRIGGER IF NOT EXISTS PERSON_UPDATE
                                    AFTER UPDATE
                                    ON PEOPLE
                                BEGIN
                                    UPDATE
                                        PEOPLE
                                    SET
                                        LAST_MODIFIED_DATE = CURRENT_DATE
                                    WHERE
                                        PERSON_ID = OLD.PERSON_ID AND LAST_MODIFIED_DATE != CURRENT_DATE;
                                END;'''

    reactionInsertTrigger = '''CREATE TRIGGER IF NOT EXISTS REACTION_INSERT
                                    AFTER INSERT
                                    ON REACTIONS
                                BEGIN
                                    UPDATE
                                        REACTIONS
                                    SET
                                        CREATED_DATE = DATETIME(CURRENT_DATE),
                                        LAST_MODIFIED_DATE = DATETIME(CURRENT_DATE)'''

    createTriggerList = [personInsertTrigger, listHeaderInertTrigger, listLinesInsertTrigger,
                            itemInsertTrigger, personUpdateTrigger, reactionInsertTrigger]

    createTablesList = [createPeopleTable, createUsersTable, createListHeadersTable,
                        createItemsTable, createListLinesTable, createReactionsTable,
                        createActivitiesTable, createLookupsTable]

    conn = None

    try:
        conn = sqlite3.connect(r'db/foodtracker.db')
        c = conn.cursor()

        for table in createTablesList:
            c.execute(table)

        for table in createTriggerList:
            c.execute(table)
        
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
