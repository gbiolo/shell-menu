
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
    along with shell-menu.  If not, see <http://www.gnu.org/licenses/>.
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
import re


# Import the sheel-menu libraries
sys.path = ([sys.path[0] + "/shell-menu"] + sys.path)
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
    with open(sys.path[1] + "/cnf/shell-menu.json", "r") as configuration:
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

    # Style parameters to default values
    vmargin = 0
    hmargin = 0
    hpadding = 3

    # If the user inserted a style configuration in the main JSON, read the
    # defined values.
    # Undefined style values will remain to the default value.
    if "style" in main_conf:
        if "vmargin" in main_conf["style"]:
            vmargin = main_conf["style"]["vmargin"]
        if "hmargin" in main_conf["style"]:
            hmargin = main_conf["style"]["hmargin"]
        if "hpadding" in main_conf["style"]:
            hpadding = main_conf["style"]["hpadding"]

    # Exit sequence to the default value and read from the configuration if
    # defined by the user.
    # The default exit sequence is the simple "0" (zero) character
    exit_key = "0"
    if "exit_key" in main_conf:
        exit_key = main_conf["exit_key"]

    # Remove environment variable into user configuration JSON and replace with
    # their values
    for variable in re.findall("\$[A-Z|_]+",
                               main_conf["configurations"][hostname][user]):
        # Remove the dollar symbol from the variable name
        variable = variable[1:]
        # Replace each environment variable used
        if variable in os.environ:
            main_conf["configurations"][hostname][user] = re.sub(
                "\$"+variable, os.environ[variable],
                main_conf["configurations"][hostname][user])

    # Open the specific configuration JSON indicated in the main configuration
    with open(main_conf["configurations"][hostname][user]) as configuration:
        menu_conf = json.load(configuration)
        # Add all menu boxes
        for menu in sorted(menu_conf["menu"].keys()):
            boxes.append(Menu(menu_conf["menu"][menu]))
        # Add all info boxes if any
        if "info" in menu_conf:
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
        question = ("{0}{1}@{2} make your choice [ \"{3}\" to exit ] : ".
                    format((' '*hmargin), getuser(), gethostname(), exit_key))
        if sys.version_info[0] == 2:
            choice = raw_input(question)
        elif sys.version_info[0] == 3:
            choice = input(question)
        if choice == exit_key:
            call("clear")
            exit()
        else:
            found = 0
            # Check each menu box if there is a command with the inserted index
            for box in boxes:
                if isinstance(box, Menu):
                    command = box.get_command(choice)
                    if command:
                        found = 1
                        call("clear")
                        # Execution of the command
                        call(command)
            # Command not found in any menu box
            if not found:
                print()
                print("{0}\"{1}\" is not a valid choice".
                      format((' '*hmargin), choice), end="\n\n")

            # Print the 'go back' message and wait until the user press the
            # ENTER button to continue
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                print((' '*hmargin) + "--------------------")
                # For Python 2.6+ the exception of SyntaxError for empty string
                # must be catched and "pass" the error
                try:
                    input((" "*hmargin) +
                          "Press ENTER to return to shell-menu")
                except SyntaxError:
                    pass
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
