/* People */
INSERT INTO 
    PEOPLE (FIRST_NAME, MIDDLE_INITIAL, LAST_NAME)
VALUES
    ('Sophia', 'G', 'Hobbes');
    
INSERT INTO
    PEOPLE (FIRST_NAME, MIDDLE_INITIAL, LAST_NAME)
VALUES
    ('Taylor', 'E', 'Hobbes');

/* Lists */
INSERT INTO
    LIST_HEADERS (DESCRIPTION, PERSON_ID)
VALUES
    ("Sophia's Food List", (select person_id from people where first_name = 'Sophia' and last_name = 'Hobbes'));
    
/* Items */
INSERT INTO
    ITEMS (DESCRIPTION)
VALUES
    ('Pineapple');
    
/* list Items */
INSERT INTO
    LIST_LINES (ITEM_ID, HEADER_ID, DAY_DT)
VALUES
    (1, 1, CURRENT_DATE);