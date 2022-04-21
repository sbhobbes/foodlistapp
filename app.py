"""
App for tracking food consumption to detect possible allergens
"""
import toga
import sqlite3
from foodtracker.sql_scripts import *
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class FoodTracker(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """

        self.db = r'src/foodtracker/db/foodtracker.db'

        main_box = toga.Box(style = Pack(direction = COLUMN))

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

        addUserButton = toga.Button(
            'Add User',
            on_press = self.IssueQuery,
            style = Pack(padding = 5)
        )

        main_box.add(firstNameBox)
        main_box.add(middleNameBox)
        main_box.add(lastNameBox)
        main_box.add(addUserButton)

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    def IssueQuery(self, widget):
        
        InsertNewPerson(self.db, self.firstNameInput.value, self.middleNameInput.value, self.lastNameInput.value)


def main():
    return FoodTracker()
