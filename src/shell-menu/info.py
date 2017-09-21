
''' shell-menu is a simplified menu for shell environment.

Description:
    The main target of the project is to provide an easy to deploy menu to use in
    shell mode, for example in case of remote SSH connection, that allow the user
    to easily execute a set of command.

    The configuration is based on two JSON format files. The first must be located
    in a subdirectory called 'cnf' inside the shell-menu.py directory.
    The second one can be saved in any directory of the system where the user that
    will execute the shell-menu.py has the read grants.

    First configuration file is the main one, and the name must be "shell-menu.json".
    The user is free to choose a name for the second one.

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
'''


import re

from box import Box


class Info( Box ):
    ''' Class that rappresent an info box, with one or more text messages
    '''

    def __init__( self, configuration ):
        ''' Read the configuration for the info box from a dictionary, passed as
        argument, and split the text into rows of a given maximum length
        '''
        # Initialization of the base object
        Box.__init__( self )

        self.title = configuration[ "title" ]

        # Full text to split in multiple lines
        unsplitted = configuration[ "text" ]

        # Maximum legnth of each line
        length = int( configuration[ "width" ], base=10 )
        if length < len( self.title ):
            length = len( self.title )
        self.size = ( length + 4 )
        Box.create_header( self )

        # Generate the rows of the box
        if len( configuration[ "text" ] ) > 1:
            for text in configuration[ "text" ]:
                self.split_and_append( text, length, "* " )
        else:
            self.split_and_append( configuration[ "text" ][ 0 ], length )

        # Closing info box
        self.rows.append( "+-" + ('-'*(length+1)) + "+" )

    def split_and_append( self, unsplitted, length, head="" ):
        ''' Method to split the info box message text into multiple lines to
        insert in the box "rows" array; all final lines must respect the given
        length.
        The parameter "head" indicates an header for the first line of the
        splitted output.
        For single text info box no header is inserted, instad for multi text info
        box each text starts with a "* " header
        '''
        # Temporary variables for line length and line content
        temp_length = 0
        temp_row    = head
        # Split the input string in words and reformat the word one by one
        for word in re.split( "\s+", unsplitted ):
            if temp_row == head:
                temp_row = ( "| " + head )
            # words with length over the line length, will be splitted into sub-words
            # and a '-' will be inserted at the end of each sub-words (except the
            # last one)
            while len( word ) > length:
                self.rows.append( self.format_string( temp_row +
                                  word[ 0:(length-temp_length-2) ] + "- |",
                                  (length+4) ) )
                word = word[ (length-temp_length-1): ]
                temp_length = 0
            # There is enought space at the end of the line to append the new word
            if ( len( word ) + temp_length + 1 ) < length:
                temp_row += word + " "
                temp_length += ( len( word ) + 1 )
            # No space for the new word, so the line must be finalized and appended
            # to the rows array of the box
            else:
                self.rows.append( self.format_string( temp_row, (length+3) ) + "|" )
                temp_row = "| " + word + " "
                temp_length = ( len( word ) + 1 )
        # Append the last line created to the array (only if not empty)
        if temp_row != "":
            self.rows.append( self.format_string( temp_row, (length+3) ) + "|" )
