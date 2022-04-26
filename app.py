"""
App for tracking food consumption to detect possible allergens
"""
#from distutils.dep_util import newer_pairwise
from operator import index
#from socket import create_connection
import toga
import sqlite3
import os
from foodtracker.sql_scripts import *
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from foodtracker.create_database import *


class FoodTracker(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        # Create database if it does not already exist
        dirname = os.path.dirname(__file__)
        self.db = os.path.join(dirname, 'db/foodlist.db')
        CreateDatabase(self.db)

        # Declare menu options
        homeCommand = toga.Command(
            self.HomeForm,
            label = 'Home',
            tooltip = 'Return to the home screen.'
        )
        addPersonCommand = toga.Command(
            self.AddPersonForm,
            label = 'New Person',
            tooltip = 'Create a new person record.'
        )
        addListHeaderCommand = toga.Command(
            self.AddListHeaderForm,
            label = 'Create New Log',
            tooltip = 'Create a new log for tracking food.'
        )
        editTablesCommand = toga.Command(
            self.EditTablesForm,
            label = 'Edit Tables',
            tooltip = 'Update data stored in various tables, such as food items, lists, etc.'
        )
        newFoodEntryCommand = toga.Command(
            self.AddListLineForm,
            label = 'New Log Entry',
            tooltip = 'Add a new food item to an existing list.'
        )
        addItemCommand = toga.Command(
            self.AddItemForm,
            label = 'New Item',
            tooltip = 'Add a new food item to the list of available food.'
        )
        addLookupCommand = toga.Command(
            self.AddLookupForm,
            label = 'Add Lookup Value',
            tooltip = 'Add a new value to the list of reaction locations.'
        )

        # Define the database path
        #self.db = r'src/foodtracker/db/foodtracker.db'
        #self.db = db

        # Declare the main box which will be used throughout the application to add and remove widgets
        # For use by the app user
        self.mainBox = toga.Box(style = Pack(direction = COLUMN))

        # This box is used later when calling edit tables
        self.editItemValuesBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        self.editTableDataBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        self.buttonsBox = toga.Box(style = Pack(direction = ROW, padding = 5))

        # Declare the widgets to add to the main box
        addFoodButton = toga.Button(
            'New Log Entry',
            on_press = self.AddListLineForm,
            style = Pack(padding = 5)
        )
        viewFoodEntries = toga.Button(
            'View Log',
            on_press = self.ViewListForm,
            style = Pack(padding = 5)
        )

        # Add the widgets to the main box
        #self.mainBox.add(addFoodButton)
        #self.mainBox.add(viewFoodEntries)
        self.buttonsBox.add(addFoodButton)
        self.buttonsBox.add(viewFoodEntries)
        self.mainBox.add(self.buttonsBox)
        
        # Create the app window and menu options
        self.commands.add(homeCommand, editTablesCommand, addPersonCommand, addListHeaderCommand, newFoodEntryCommand,
                            addItemCommand, addLookupCommand)
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.mainBox
        self.main_window.show()


    # Function to call the query to insert a new person record into the DB
    def InsertPersonQuery(self, widget):
        InsertNewPerson(self.db, self.firstNameInput.value, self.middleNameInput.value, self.lastNameInput.value)
        self.HomeForm(self)


    # Display the screen which allows the user to insert a new item record
    def AddItemForm(self, widget):

        # Remove whatever widgets are currently on the screen
        self.RemoveChildren()

        # Declare widgets for use on the item insert form and add to individual boxes for layout control
        itemDescriptionLabel = toga.Label(
            'Food: ',
            style = Pack(padding = (0, 5))
        )
        self.itemDescriptionInput = toga.TextInput(style = Pack(flex = 1))
        itemDescriptionBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        itemDescriptionBox.add(itemDescriptionLabel)
        itemDescriptionBox.add(self.itemDescriptionInput)

        # Declare additional widgets for use on the item insert form
        addItemButton = toga.Button(
            'Add Food',
            on_press = self.InsertItemQuery,
            style = Pack(padding = 5)
        )

        # Declare the item insert form box and add all widgets to it
        addItemBox = toga.Box(style = Pack(direction = COLUMN))
        addItemBox.add(itemDescriptionBox)
        #addItemBox.add(addItemButton)
        
        # Put the item insert form into the main box for display to the user
        self.buttonsBox.add(addItemButton)
        self.mainBox.add(addItemBox)
        self.mainBox.add(addItemButton)


    # Display the screen which allows the user to insert a new person record
    def AddPersonForm(self, widget):

        # Remove whatever widgets are currently on the screen
        self.RemoveChildren()

        # Declare widgets for use on the person insert form and add to individual boxes for layout control
        firstNameLabel = toga.Label(
            'First Name',
            style = Pack(padding = (0, 5))
        )
        self.firstNameInput = toga.TextInput(style = Pack(flex = 1))
        firstNameBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        firstNameBox.add(firstNameLabel)
        firstNameBox.add(self.firstNameInput)
        middleNameLabel = toga.Label(
            'Middle Initial',
            style = Pack(padding = (0, 5))
        )
        self.middleNameInput = toga.TextInput(style = Pack(flex = 1))
        middleNameBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        middleNameBox.add(middleNameLabel)
        middleNameBox.add(self.middleNameInput)
        lastNameLabel = toga.Label(
            'Last Name',
            style = Pack(padding = (0, 5))
        )
        self.lastNameInput = toga.TextInput(style = Pack(flex = 1))
        lastNameBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        lastNameBox.add(lastNameLabel)
        lastNameBox.add(self.lastNameInput)

        # Declare additional widgets for use on the person insert form
        addUserButton = toga.Button(
            'Add User',
            on_press = self.InsertPersonQuery,
            style = Pack(padding = 5)
        )

        # Declare the person insert form box and add all widgets to it
        addUserBox = toga.Box(style = Pack(direction = COLUMN))
        addUserBox.add(firstNameBox)
        addUserBox.add(middleNameBox)
        addUserBox.add(lastNameBox)
        #addUserBox.add(addUserButton)

        # Put the person insert form into the main box for display to the user
        self.buttonsBox.add(addUserButton)
        self.mainBox.add(addUserBox)
        self.mainBox.add(self.buttonsBox)


    # Display the screen which allows the user to insert a new list header
    def AddListHeaderForm(self, widget):

        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Retrieve list of people from the database
        self.peopleIDList = self.GetPeopleQuery()

        headerDescriptionLabel = toga.Label(
            'List Name: ',
            style = Pack(padding = (0, 5))
        )
        self.headerDescriptionInput = toga.TextInput(style = Pack(flex = 1))
        headerDescriptionBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        headerDescriptionBox.add(headerDescriptionLabel)
        headerDescriptionBox.add(self.headerDescriptionInput)

        headerPersonIDLabel = toga.Label(
            'Person: ',
            style = Pack(padding = (0, 5))
        )
        self.peopleList = []
        for row in self.peopleIDList:
            self.peopleList.append(row[1])
        self.headerPersonIDInput = toga.Selection(items = self.peopleList)
        headerPersonIDBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        headerPersonIDBox.add(headerPersonIDLabel)
        headerPersonIDBox.add(self.headerPersonIDInput)

        submitButton = toga.Button(
            'Submit',
            on_press = self.InsertListHeaderQuery,
            style = Pack(padding = 5)
        )

        self.buttonsBox.add(submitButton)

        self.mainBox.add(headerDescriptionBox)
        self.mainBox.add(headerPersonIDBox)
        #self.mainBox.add(submitButton)
        self.mainBox.add(self.buttonsBox)


    # Insert a new list into the database
    def InsertListHeaderQuery(self, widget):
        print(self.headerPersonIDInput.value)
        for value in self.peopleList:
            if self.headerPersonIDInput.value == value:
                index = self.peopleList.index(value)
                selectedPerson = self.peopleIDList[index][0]

        InsertNewListHeader(self.db, selectedPerson, self.headerDescriptionInput.value)
        #print(self.peopleIDList[index][0])  # This should be the PERSON_ID to send back to the SQL to update the DB
        self.HomeForm(self)


    # Display the screen which allows the user to create a new list line
    def AddListLineForm(self, widget):

        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Get list of items
        self.itemIDList = self.GetItemsQuery()
        print(self.itemIDList)
        self.itemList = []
        for row in self.itemIDList:
            self.itemList.append(row[1])

        self.listHeaderIDList = self.GetListHeadersQuery()
        print(self.listHeaderIDList)
        self.listHeaderList = []
        for row in self.listHeaderIDList:
            self.listHeaderList.append(row[1])
        
        # Declare widgets for use on the insert list line form
        listHeaderReferenceLabel = toga.Label(
            'List Name: ',
            style = Pack(padding = 5)
        )
        self.listHeaderReferenceInput = toga.Selection(items = self.listHeaderList)
        listHeaderReferenceBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        listHeaderReferenceBox.add(listHeaderReferenceLabel)
        listHeaderReferenceBox.add(self.listHeaderReferenceInput)
        listLineDateLabel = toga.Label(
            'Date: ',
            style = Pack(padding = 5)
        )
        self.listLineDateInput = toga.DatePicker()
        listLineDateBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        listLineDateBox.add(listLineDateLabel)
        listLineDateBox.add(self.listLineDateInput)
        listLineItemIDLabel = toga.Label(
            'Item: ',
            style = Pack(padding = 5)
        )
        self.listLineItemIDInput = toga.Selection(items = self.itemList)
        listLineAddItemButton = toga.Button(
            '+',
            on_press = self.AddItemForm,
            style = Pack(padding = 0.5)
        )
        listLineItemBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        listLineItemBox.add(listLineItemIDLabel)
        listLineItemBox.add(self.listLineItemIDInput)
        #listLineItemBox.add(listLineAddItemButton)

        listLineButton = toga.Button(
            'Add to list',
            on_press = self.InsertListLineQuery,
            style = Pack(padding = 0)
        )

        self.buttonsBox.add(listLineAddItemButton)
        self.buttonsBox.add(listLineButton)

        self.mainBox.add(listHeaderReferenceBox)
        self.mainBox.add(listLineDateBox)
        self.mainBox.add(listLineItemBox)
        self.mainBox.add(self.buttonsBox)
        #self.mainBox.add(listLineButton)


    # Display the screen which allows the user to create a new lookup list value
    def AddLookupForm(self, widget):

        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Declare widgets for use on the insert lookup values form
        lookupDescriptionLabel = toga.Label(
            'Lookup Value: ',
            style = Pack(padding = 5)
        )
        self.lookupDescriptionInput = toga.TextInput(style = Pack(flex = 1))
        lookupDescriptionBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        lookupDescriptionBox.add(lookupDescriptionLabel)
        lookupDescriptionBox.add(self.lookupDescriptionInput)
        
        addLookupButton = toga.Button(
            'Add to Values',
            on_press = self.InsertLookupQuery,
            style = Pack(padding = 0.5)
        )

        self.mainBox.add(lookupDescriptionBox)
        #self.mainBox.add(addLookupButton)
        self.buttonsBox.add(addLookupButton)
        self.mainBox.add(self.buttonsBox)

    
    # Insert a new list line into the database
    def InsertListLineQuery(self, widget):
        print(self.listLineItemIDInput.value)

        for value in self.listHeaderList:
            if self.listHeaderReferenceInput.value == value:
                index = self.listHeaderList.index(value)
                selectedHeader = self.listHeaderIDList[index][0]

        for value in self.itemList:
            if self.listLineItemIDInput.value == value:
                index = self.itemList.index(value)
                selectedItem = self.itemIDList[index][0]

        InsertNewListLine(self.db, selectedHeader, selectedItem, self.listLineDateInput.value)
        self.HomeForm(self)


    # Display the home screen
    def HomeForm(self, widget):

        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Declare the widgets to add to the main box
        addFoodButton = toga.Button(
            'New Log Entry',
            on_press = self.AddListLineForm,
            style = Pack(padding = 5)
        )
        viewFoodEntries = toga.Button(
            'View Log',
            on_press = self.ViewListForm,
            style = Pack(padding = 5)
        )

        # Add the widgets to the main box
        #self.mainBox.add(addFoodButton)
        #self.mainBox.add(viewFoodEntries)
        self.buttonsBox.add(addFoodButton)
        self.buttonsBox.add(viewFoodEntries)
        self.mainBox.add(self.buttonsBox)

    
    # Display the screen which allows the user to view historical entries
    def ViewListForm(self, widget):
        
        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Declare widgets for use on the view history form
        fromDateLabel = toga.Label(
            'From Date: ',
            style = Pack(padding = 5)
        )
        self.fromDateInput = toga.DatePicker()
        fromDateBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        fromDateBox.add(fromDateLabel)
        fromDateBox.add(self.fromDateInput)
        toDateLabel = toga.Label(
            'To Date: ',
            style = Pack(padding = 5)
        )
        self.toDateInput = toga.DatePicker()
        toDateBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        toDateBox.add(toDateLabel)
        toDateBox.add(self.toDateInput)

        searchButton = toga.Button(
            'Search',
            on_press = self.GetHistoryQuery,
            style = Pack(padding = 5)
        )

        self.mainBox.add(fromDateBox)
        self.mainBox.add(toDateBox)
        #self.mainBox.add(searchButton)
        self.buttonsBox.add(searchButton)
        self.mainBox.add(self.buttonsBox)

    
    # Display the screen which allows the user to update table values
    def EditTablesForm(self, widget):
        
        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Retrieve list of table names from the database
        tableNamesList = self.GetTableNamesQuery()
        
        tableNamesListModified = []
        for name in tableNamesList:
            tableNamesListModified.append(name[0])

        # Add widgets to allow the user to choose which table to edit
        tablePickerLabel = toga.Label(
            'Pick a table to update: ',
            style = Pack(padding = 5)
        )
        self.tablePickerInput = toga.Selection(
            items = tableNamesListModified, 
            on_select = self.EditTableDataForm
        )
        tablePickerBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        tablePickerBox.add(tablePickerLabel)
        tablePickerBox.add(self.tablePickerInput)
        self.editTableDataBox.add(tablePickerBox)

        # editTableButton = toga.Button(
        #     'Edit Table',
        #     on_press = self.EditTableDataForm,
        #     style = Pack(padding = 5)
        # )
        
        self.mainBox.add(tablePickerBox)
        #self.mainBox.add(editTableButton)


    def DeleteTableDataQuery(self, widget):

        # Confirm delete
        confirmDeleteLabel = toga.Label(
            'Type DELETE to confirm.',
            style = Pack(padding = 5, color = 'red')
        )
        self.confirmDeleteInput = toga.TextInput(style = Pack(padding = 5, flex = 1))
        confirmDeleteBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        confirmDeleteBox.add(confirmDeleteLabel)
        confirmDeleteBox.add(self.confirmDeleteInput)
        
        confirmDeleteSubmitButton = toga.Button(
            'Confirm',
            on_press = self.ValidateDataDeletion,
            style = Pack(padding = 5)
        )
        confirmDeleteBox.add(confirmDeleteSubmitButton)

        self.mainBox.add(confirmDeleteBox)
        #self.mainBox.add(confirmDeleteSubmitButton)
        #self.mainBox.add(confirmDeleteSubmitButton)
        self.mainBox.add(self.buttonsBox)


    def ValidateDataDeletion(self, widget):
        
        # Check to ensure that the word DELETE was typed into the text input
        if self.confirmDeleteInput.value == 'DELETE':
            if self.tablePickerInput.value == 'ITEMS':
                DeleteFromTable(self.db, 'ITEMS', 'ITEM_ID', self.tableDataInput.selection.ITEM_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'LIST_HEADERS':
                DeleteFromTable(self.db, 'LIST_HEADERS', 'HEADER_ID', self.tableDataInput.selection.HEADER_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'LIST_LINES':
                DeleteFromTable(self.db, 'LIST_LINES', 'LINE_ID', self.tableDataInput.selection.LINE_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'LOOKUPS':
                DeleteFromTable(self.db, 'LOOKUPS', 'LOOKUP_ID', self.tableDataInput.selection.LOOKUP_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'PEOPLE':
                DeleteFromTable(self.db, 'PEOPLE', 'PERSON_ID', self.tableDataInput.selection.PERSON_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'REACTIONS':
                DeleteFromTable(self.db, 'REACTIONS', 'REACTION_ID', self.tableDataInput.selection.REACTION_ID)
                self.EditTablesForm(self)
            if self.tablePickerInput.value == 'USERS':
                DeleteFromTable(self.db, 'USERS', 'USER_ID', self.tableDataInput.selection.USER_ID)
                self.EditTablesForm(self)
        else:
            errorMessageLabel = toga.Label(
                'Did you type "DELETE" in all caps?', 
                style = Pack(padding = 5, color = 'red')
            )
            
            self.mainBox.add(errorMessageLabel)

    
    def EditTableDataForm(self, widget):
        
        # Remove whatever widgets are currently being displayed
        #self.RemoveChildren()
        for child in reversed(self.editTableDataBox.children):
            self.editTableDataBox.remove(child)

        for child in reversed(self.buttonsBox.children):
            self.buttonsBox.remove(child)

        # Set table up and pull data based on user selection
        # if self.tablePickerInput.value == 'ITEMS':
        #     columns = ['ITEM_ID', 'DESCRIPTION', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'LIST_HEADERS':
        #     columns = ['HEADER_ID', 'DESCRIPTION', 'PERSON_ID', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'LIST_LINES':
        #     columns = ['LINE_ID', 'HEADER_ID', 'ITEM_ID', 'DATE', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'LOOKUPS':
        #     columns = ['LOOKUP_ID', 'DESCRIPTION', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'PEOPLE':
        #     columns = ['PERSON_ID', 'FIRST_NAME', 'LAST_NAME', 'FULL_NAME', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'REACTIONS':
        #     columns = ['REACTION_ID', 'PERSON_ID', 'DATE', 'DESCRIPTION', 'LOCATION', 'CREATED_BY', 'CREATED_DATE', 'LAST_MODIFIED_BY', 'LAST_MODIFIED_DATE']
        # elif self.tablePickerInput.value == 'USERS':
        #     columns = ['USER_ID', 'PERSON_ID', 'USERNAME', 'CREATED_DATE', 'LAST_MODIFIED_DATE']

        self.tableData = SelectEntireTable(self.db, self.tablePickerInput.value)
        
        if self.tablePickerInput.value == 'PEOPLE':
            self.tableDataList = []
            for row in self.tableData:
                self.tableDataList.append(row[3])
        elif self.tablePickerInput.value == 'USERS':
            self.tableDataList = []
            for row in self.tableData:
                self.tableDataList.append(row[2])
        elif self.tablePickerInput.value == 'LIST_LINES':
            self.tableDataItemIDList = []
            self.tableDataDateList = []
            for row in self.tableData:
                self.tableDataItemIDList.append(row[2])
                self.tableDataDateList.append(row[3])
        else:
            self.tableDataList = []
            for row in self.tableData:
                self.tableDataList.append(row[1])

        #self.tableDataInput = toga.Table(columns, data = tableData, accessors = columns)
        if self.tablePickerInput.value == 'LIST_LINES':
            self.tableDataItemInput = toga.Selection(items = self.tableDataItemIDList, on_select = self.EditTable)
            self.tableDataDateInput = toga.Selection(items = self.tableDataDateList, on_select = self.EditTable)
            self.itemDescriptionInput = toga.TextInput(style = Pack(flex = 1))
            self.dateDescriptionInput = toga.TextInput(style = Pack(flex = 1))
            self.editTableDataBox.add(self.tableDataItemInput)
            self.editTableDataBox.add(self.itemDescriptionInput)
            self.editTableDataBox.add(self.tableDataDateInput)
            self.editTableDataBox.add(self.dateDescriptionInput)
        else:
            self.tableDataInput = toga.Selection(items = self.tableDataList, on_select = self.EditTable)
            self.descriptionInput = toga.TextInput(style = Pack(flex = 1))
            self.editTableDataBox.add(self.tableDataInput)
            self.editTableDataBox.add(self.descriptionInput)
        
        # editSelectionButton = toga.Button(
        #     'Edit Selected Item',
        #     on_press = self.EditTable,
        #     style = Pack(padding = 5)
        # )

        deleteFromTableButton = toga.Button(
            'Delete',
            on_press = self.DeleteTableDataQuery,
            style = Pack(padding = 5)
        )
        updateTableDataButton = toga.Button(
            'Update',
            on_press = self.UpdateTableDataQuery,
            style = Pack(padding = 5)
        )
        cancelButton = toga.Button(
            'Cancel',
            on_press = self.HomeForm,
            style = Pack(padding = 5)
        )
        #self.descriptionInput = toga.TextInput(style = Pack(flex = 1))
        #self.editTableDataBox.add(self.tableDataInput)
        #self.editTableDataBox.add(self.descriptionInput)
        #self.editTableDataBox.add(deleteFromTableButton)
        self.buttonsBox.add(updateTableDataButton)
        self.buttonsBox.add(deleteFromTableButton)
        self.buttonsBox.add(cancelButton)
        
        #self.mainBox.add(self.tableDataInput)
        #self.mainBox.add(editSelectionButton)
        #self.mainBox.add(deleteFromTableButton)
        self.mainBox.add(self.editTableDataBox)
        self.mainBox.add(self.buttonsBox)


    def GetTableRecordID(self):
        tableRecordID = None
        for value in self.tableDataList:
            if self.tableDataInput.value == value:
                index = self.tableDataList.index(value)
                tableRecordID = self.tableData[index][0]
        
        return tableRecordID


    def UpdateTableDataQuery(self, widget):
        pass


    def EditTable(self, widget):

        # for child in reversed(self.editItemValuesBox.children):
        #     self.editItemValuesBox.remove(child)
        
        # for child in reversed(self.buttonsBox.children):
        #     self.buttonsBox.remove(child)

        # itemIDLabel = toga.Label(
        #     self.GetTableRecordID(),
        #     style = Pack(padding = 5)
        # )
        # descriptionLabel = toga.Label(
        #     'Item Description: ',
        #     style = Pack(padding = 5)
        # )
        #descriptionInput = toga.TextInput(style = Pack(flex = 1))
        self.descriptionInput.value = self.tableDataInput.value
        #editItemValuesBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        #self.editItemValuesBox.add(itemIDLabel)
        #self.editItemValuesBox.add(descriptionLabel)
        #self.editItemValuesBox.add(descriptionInput)
        #self.editTableDataBox.add(descriptionInput)
        
        #self.mainBox.add(self.editItemValuesBox)
        #self.mainBox.add(self.editTableDataBox)


    # Removes all widgets from the current screen
    def RemoveChildren(self):
        for child in reversed(self.mainBox.children):
            self.mainBox.remove(child)

        for child in reversed(self.buttonsBox.children):
            self.buttonsBox.remove(child)


    # Insert a new food item
    def InsertItemQuery(self, widget):
        InsertNewItem(self.db, self.itemDescriptionInput.value)
        self.HomeForm(self)

    
    # Insert a new lookup value
    def InsertLookupQuery(self, widget):
        InsertNewLookups(self.db, self.lookupDescriptionInput.value)
        self.HomeForm(self)


    # Retrieve a list of names from the people table and return to calling function
    def GetPeopleQuery(self):
        peopleList = SelectPeople(self.db)
        return peopleList


    # Retrieve a list of items from the items table and return to calling function
    def GetItemsQuery(self):
        itemList = SelectItems(self.db)
        return itemList

    
    # Retrieve list of list headers from the list headers table and return to calling function
    def GetListHeadersQuery(self):
        listHeadersList = SelectListHeaders(self.db)
        return listHeadersList

    
    # Retrieve a list of table names from the database
    def GetTableNamesQuery(self):
        tableNamesList = SelectTableNames(self.db)
        return tableNamesList


    # Retrieve a history view of log entries
    def GetHistoryQuery(self, widget):
        history = SelectHistory(self.db, self.fromDateInput.value, self.toDateInput.value)
        
        # Remove whatever widgets are currently being displayed
        self.RemoveChildren()

        # Set up table widget to display the data from the table view
        columns = ['Date', 'Food']
        historyTable = toga.Table(columns, data = history)
        newSearchButton = toga.Button(
            'New Search',
            on_press = self.ViewListForm,
            style = Pack(padding = 5)
        )
        returnHomeButton = toga.Button(
            'Home',
            on_press = self.HomeForm,
            style = Pack(padding = 5)
        )
        buttonsBox = toga.Box(style = Pack(direction = ROW, padding = 5))
        buttonsBox.add(newSearchButton)
        buttonsBox.add(returnHomeButton)

        self.mainBox.add(historyTable)
        self.mainBox.add(buttonsBox)

def main():
    return FoodTracker()