# MVC Banking App

## Overview
The toy banking app is used to demonstrate the Model-View-Controller architecture. It is comprised of a GUI and Database manager. The GUI is composed of an Account "View", which is populated from the database or "Model". The buttons on the GUI, the "Controller", are responsible for making changes to certain accounts. Once changes are made, the view is updated to reflect the most current view of the model.

## Requirements 
These are the versions the software was built with

 - Python 3.8.12
 - numpy 1.21.5
 - PyQt6 6.1.0
 - pandas 1.4.1
 
 Other required libraries:
 - sqlite3 (connect)
 - typing (List, Tuple)
 - contextlib (contextmanager)

## Running the App
The app can be run by pulling the code from this repository and running:

Mac/Linux  `$ python BankAppUI.py`

Windows    `$ python.exe -m BankAppUI.py`

Depending on what packages you have installed through pip or conda, you may need to install dependencies before running the application. Most likely you will need to install PyQt6:

Mac/Linux  `$ python pip install pyqt6 pyqt6-tools`

Windows    `$ python.exe -m pip install pyqt6 pyqt6-tools`
