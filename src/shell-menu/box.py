
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


class Box:
    """This class rappresent a generic object "Box".

    A "Box" object may contains a menu o one (or even more) info.
    """

    def __init__(self):
        """Initialization of an empty box.

        The generic attributes are:
            rows  : array containing the rows that compose the box, don't care
                    if it's a menu or an info box, with header and footer
            size  : width of the box expressed in character
            title : title of the box
            index : index used by the method get_row to keep the index of the
                    last row returned to the caller
        """
        self.rows = []
        self.size = 0
        self.title = ""
        self.index = 0

    def format_string(self, unformatted, length, allign="sx"):
        """Function to format a string to a given length and allignment.

        Input parameters are the following:
            unformatted : string to format
            length      : final length of the formatted string; in case of
                          input string longer than the final length, the final
                          string will be the same of the input one
            allign      : allignment of the final string; allowed values:
                              - sx     : left allignment   (default value)
                              - dx     : right allignment
                              - center : centred string
        Return value is the formatted string.
        """
        if len(unformatted) >= length:
            return unformatted
        formatted = ""
        spaces = (length - len(unformatted))
        if allign == "sx":
            formatted = (unformatted + (' ' * spaces))
        elif allign == "dx":
            formatted = ((' ' * spaces) + unformatted)
        elif allign == "center":
            spaces_sx = int(spaces / 2)
            spaces_dx = (int(spaces / 2) + (spaces % 2))
            formatted = ((' ' * spaces_sx) + unformatted + (' ' * spaces_dx))
        return formatted

    def create_header(self):
        """Create the header for the box reporting the name (centered).

        If the header already exists, the whole content of the "rows" array
        will be erased and replaced by a new header
        """
        if len(self.rows) > 0:
            self.rows = []
        self.rows.append("+-" + ('-'*(self.size-3)) + "+")
        self.rows.append("|" + self.format_string(self.title, (self.size-2),
                                                   "center") + "|")
        self.rows.append("+-" + ('-'*(self.size-3)) + "+")

    def get_row(self):
        """Method that return an element (row) from the "rows" array.

        If the index is over the array elements number, the method return a
        string of the same size of a row but composed by only spaces (useful to
        create many levels shell-menu)
        """
        if self.index <= (len(self.rows) - 1):
            self.index += 1
            return self.rows[(self.index - 1)]
        else:
            return None
