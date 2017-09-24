#! /usr/bin/env python3

"""shell-menu is a simplified menu for shell environment.

Description:
    The main target of the project is to provide an easy to deploy menu to use
    in shell mode, for example in case of remote SSH connection, that allows
    the user to easily execute a set of command.

    The configuration is based on two JSON format files. The first must be
    located in a subdirectory called 'cnf' inside the shell-menu.py directory.
    The second one can be saved in any directory of the system where the user
    that will execute the shell-menu.py has the read grants.

    First configuration file is the main one, and the name must be
    "shell-menu.json". The user is free to choose a name for the second one.

Author:
    Giuseppe Biolo  < giuseppe.biolo@gmail.com > < https://github.com/gbiolo >

License:
    This file is part of shell-menu.

    shell-menu is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    shell-menu is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""


# Compatibility with Python 2.6+ and Python 3.3+
from __future__ import print_function
from __future__ import with_statement

import json
from socket import gethostname
from getpass import getuser
from subprocess import call
import sys
import termios
import os


# Import the sheel-menu libraries
sys.path.append(os.getcwd() + "/shell-menu")
from menu import Menu
from info import Info

# Execute only in interactive mode
if __name__ == "__main__":

    # Empty boxes collection
    boxes = []

    # Dictionaries containing the configuration JSONs
    main_conf = None
    menu_conf = None

    # Open and load the main configuration JSON
    with open(os.getcwd() + "/cnf/shell-menu.json", "r") as configuration:
        main_conf = json.load(configuration)

    # Check if the user has defined a configuration file for the current
    # hostname
    # If there is no configuration, it try to search the generic configuration,
    # marked by the "*"
    hostname = gethostname()
    if hostname not in main_conf["configurations"]:
        if "*" in main_conf["configurations"]:
            hostname = "*"
        else:
            print("No configuration for the current hostname (" +
                  hostname + ")")
            exit()

    # Check if the user has defined a configuration file for the current user
    # If there is no configuration, it try to search the generic configuration,
    # marked by the "*"
    user = getuser()
    if user not in main_conf["configurations"][hostname]:
        if "*" in main_conf["configurations"][hostname]:
            user = '*'
        else:
            print("No configuration for the current user (" + user + ")")
            exit()

    # Extract from the configuration JSON the format fields, and convert the
    # text values into numeric (int) values
    vmargin = main_conf["vmargin"]
    hmargin = main_conf["hmargin"]
    hpadding = main_conf["hpadding"]

    # Open the specific configuration JSON indicated in the main configuration
    with open(main_conf["configurations"][hostname][user]) as configuration:
        menu_conf = json.load(configuration)
        # Add all menu boxes
        for menu in sorted(menu_conf["menu"].keys()):
            boxes.append(Menu(menu_conf["menu"][menu]))
        # Add all info boxes
        for info in sorted(menu_conf["info"].keys()):
            boxes.append(Info(menu_conf["info"][info]))

    # Till the end of the world... or the user insert the exit choice :)
    while True:

        # Reset each box index
        for box in boxes:
            box.index = 0

        # Call to clear screen
        call("clear")

        # Print the menu global title (main configuration JSON)
        print(("\n"*vmargin) + (' '*hmargin) + menu_conf["title"], end="\n\n")

        # Print, line by line, every box (menu box before, info box after)
        completed = 0
        while completed < len(boxes):
            completed = 0
            print((' '*hmargin), end='')
            for box in boxes:
                row = box.get_row()
                if row:
                    print(row, end=(' '*hpadding))
                else:
                    print((' '*box.size), end=(' '*hpadding))
                    completed += 1
            print('', end="\n")

        # Ask the user for the index of the command to execute
        choice = str(input("{0}{1}@{2} make your choice [ \"{3}\" to exit ] : ".
                     format((' '*hmargin), getuser(), gethostname(),
                            main_conf["exit_key"])))
        if choice == main_conf["exit_key"]:
            call("clear")
            exit()
        else:
            found = 0
            # For each menu box check if there is a command with the inserted index
            for box in boxes:
                if isinstance(box,Menu):
                    command = box.get_command( choice )
                    if command:
                        found = 1
                        call( "clear" )
                        # Execution of the command
                        call( command )
            # Command not found in any menu box
            if not found:
                print()
                print(  "{}\"{}\" is not a valid choice".
                       format( (' '*hmargin), choice ), end="\n\n" )

            # Print the 'go back' message and wait until the user press the
            # ENTER button to continue
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                print( (' '*hmargin) + "--------------------" )
                # For Python 2.6+ must catch the exception of SyntaxError for empty
                # string and "pass" the error
                try:
                    input( (' '*hmargin) + "Press ENTER to return to shell-menu" )
                except SyntaxError:
                    pass
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
