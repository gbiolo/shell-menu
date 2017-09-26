
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


import re

from box import Box


class Menu(Box):
    """Class that rappresent a menu box."""

    def __init__(self, configuration):
        """Initialization of the menu box object.

        The initialization add to the box the attribute "links", a dictionary
        containing all commands indicated into the user configuration JSON.
        The dictionary uses as keys the indexes of the commands, and as values
        the commands to execute (expressed as single string)
        """
        # Initialization of the base object
        Box.__init__(self)
        self.title = configuration["title"]
        # Empty dictionary initialization
        self.links = {}
        # External commands index string maximum length
        commands = configuration["commands"]
        num_commands = len(commands)
        index_length = 1
        while num_commands >= 10:
            index_length += 1
            num_commands = int(num_commands / 10)
        # Box size, calculated on length of menu name and on length of all
        # command names
        header_length = len(self.title) + 2
        for command in commands:
            command_length = (len(command["name"]) + index_length + 4)
            if command_length > header_length:
                header_length = command_length
        self.size = (header_length + 3)
        Box.create_header(self)
        # Create all menu rows that will be inserted into the array "rows"
        # Then header indicating the box name will be added by the base class
        # Then closing line will be added by the base class too
        index = configuration["base"]
        for command in commands:
            index_str = self.format_string(str(index), index_length, "dx")
            self.rows.append("| " + self.format_string(index_str + ") " +
                             command["name"] + " ", header_length, "sx") + '|')
            self.links[str(index)] = command["command"]
            index += 1
        self.rows.append("+-" + ('-'*header_length) + "+")

    def get_command(self, index):
        """Method that return an array containing the command to execute.

        The command string, from the JSON, will be splitted by spaces (the
        first element is the program, the following are the arguments).
        If the "index" argument value is not a valid key for the links
        dictionary, the method will return the value "None" (no command with
        the passed index)
        """
        if index in self.links:
            return re.split("\s+", self.links[index])
        return None
