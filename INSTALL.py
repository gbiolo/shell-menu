
''' shell-menu is a simplified menu for shell environment.

Description:
    The main target of the project is to provide an easy to deploy menu to use in
    shell mode, for example in case of remote SSH connection, that allows the user
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


# Compatibility with Python 2.6+ and Python 3.3+
from __future__ import print_function

import sys
import os
import shutil
import re
from subprocess import call


def ask_user( question ):
    ''' Function to ask something to user in interactive mode
    The only parameter to provide is the question for the user, and the return
    value is the user answer.
    '''
    answer = None
    if sys.version_info.major == 2:
        answer = raw_input( question )
    elif sys.version_info.major == 3:
        answer = input( question )
    return answer

def copy_file( source_file, destination ):
    ''' Function to copy a givven file to a givven path
    The two arguments that must be provided are:
        - source_file : file name, with absolute system path, of the new file
        - destination : absolute path of the target directory
    If it's already present in the destination directory a file with the same
    name of the new one, the old file will be lost
    '''
    if not os.path.exists( destination ):
        try:
            print( "Creating the destination path " + destination )
            os.mkdir( destination )
        except OSError:
            print( "Error in creation of destination path " + destination )
            exit()
    filename = re.split( "/", source_file ).pop()
    if os.path.exists( destination + "/" + filename ):
        print( "Updating ", end='' )
    else:
        print( "Copying ", end='' )
    print( "file {0}/{1}".format( destination, filename ) )
    try:
        shutil.copyfile( source_file, destination + "/" + filename )
    except OSError:
        print( "Error in creation of {0}/{1}".format( destination, filename ) )
        exit()


# Execute only in interactive mode
if __name__ == "__main__":

    # Actual python interpreter used to execute this installer
    interpreter_path = sys.executable

    # Local absolute path
    local_path = os.getcwd()

    # Ask installation path to the user
    destination_path = ask_user( "Full path of the directory where install shell-menu (must exists) : " )
    destination_path = ( destination_path + "/shell-menu" )

    # Mode flags
    update_mode  = False

    # Check if the installation directory exists
    if os.path.isdir( destination_path ):
        # Update mode or directory already present
        if os.path.exists( destination_path + "/shell-menu.py" ):
            print( "Installation path already contains an installation of shell-menu" )
            update_ask = ask_user( "Do you want to continue in update mode? [Y/n] " )
            if update_ask == "Y" or update_ask == "":
                update_mode = True
            else:
                print( "Please remove installation directory and repeat the installation procedure" )
                exit()
        else:
            print( "Installation path already exists. Please remove and repeat the installation procedure.")
    else:
        # Normal installation
        print( "Installation path doesn't exists. It will be created." )
        try:
            os.mkdir( destination_path )
        except OSError:
            print( "Error in install directory creation.")
            exit()

    # Copy main source file inserting the right environment
    print( "Set " + interpreter_path + " as interpreter" )
    print( "Creating source file " + destination_path + "/shell-menu.py" )
    with open( local_path + "/src/shell-menu.py", "r" ) as in_handler:
        with open( destination_path + "/shell-menu.py", "w" ) as out_handler:
            for line in in_handler:
                if re.match( "^#! ", line ):
                    print( "#! " + interpreter_path, end="\n", file=out_handler )
                else:
                    print( line, end='', file=out_handler )
    call( [ "chmod", "u+x", destination_path + "/shell-menu.py" ])

    # Copy other source files
    for src_file in os.listdir( local_path + "/src/shell-menu" ):
        if re.search( "\.py$", src_file ):
            if os.path.isfile( local_path + "/src/shell-menu/" + src_file ):
                copy_file( local_path + "/src/shell-menu/" + src_file,
                           destination_path + "/shell-menu" )

    # Copy LICENSE, README.md, CHANGELOG
    for text_file in "LICENSE", "README.md", "CHANGELOG":
        copy_file( local_path + "/" + text_file, destination_path )

    # Copy configuration files only if not in update mode
    if not update_mode:
        for cnf_file in os.listdir( local_path + "/cnf" ):
            if re.search( "\.json$", cnf_file ):
                if os.path.isfile( local_path + "/cnf/" + cnf_file ):
                    copy_file( local_path + "/cnf/" + cnf_file,
                    destination_path + "/cnf" )
