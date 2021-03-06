CREATE TABLE IF NOT EXISTS PEOPLE (
    PERSON_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    FIRST_NAME VARCHAR(40),
    MIDDLE_INITIAL VARCHAR(1),
    LAST_NAME VARCHAR(40),
    FULL_NAME VARCHAR(80),
    CREATED_BY INTEGER REFERENCES USERS (USER_ID),
    CREATED_DATE DATE,
    LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
    LAST_MODIFIED_DATE DATE
);

CREATE TABLE IF NOT EXISTS USERS (
    USER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    PERSON_ID INTEGER REFERENCES PEOPLE (PERSON_ID),
    USERNAME VARCHAR(40),
    PASSWORD VARCHAR(40),
    CREATED_DATE DATE,
    LAST_MODIFIED_DATE DATE
);

CREATE TABLE IF NOT EXISTS LIST_HEADERS (
    HEADER_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    DESCRIPTION VARCHAR(40),
    PERSON_ID INTEGER REFERENCES PEOPLE (PERSON_ID),
    CREATED_BY INTEGER REFERENCES USERS (USER_ID),
    CREATED_DATE DATE,
    LAST_MODIFIED_BY REFERENCES USERS (USER_ID),
    LAST_MODIFIED_DATE DATE
);

CREATE TABLE IF NOT EXISTS ITEMS (
    ITEM_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    DESCRIPTION VARCHAR(40),
    CREATED_BY INTEGER REFERENCES USERS (USER_ID),
    CREATED_DATE DATE,
    LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
    LAST_MODIFIED_DATE DATE
);

CREATE TABLE IF NOT EXISTS LIST_LINES (
    LINE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    HEADER_ID INTEGER REFERENCES LIST_HEADERS (HEADER_ID),
    ITEM_ID INTEGER REFERENCES ITEMS (ITEM_ID),
    DAY_DT DATE,
    CREATED_BY INTEGER REFERENCES USERS (USER_ID),
    CREATED_DATE DATE,
    LAST_MODIFIED_BY INTEGER REFERENCES USERS (USER_ID),
    LAST_MODIFIED_DATE DATE
);


DELETE FROM ITEMS;
delete from list_headers;
delete from users;
delete from people;
drop table items;
drop table list_headers;
drop table list_lines;
drop table people;
drop table users;