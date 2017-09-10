#! /usr/bin/env python3

''' shell-menu is a simple menu for Unix-like systems (Linux/HP-UX/SunOS/etc).

Description:
    The main target of the project is to provide an easy to deploy menu to use in
    shell mode, for example in case of remote SSH connection, that allow the user
    to easily execute a set of command.

    The configuration is based on two JSON format files. The first must be located
    in a subdirectory called 'cnf' inside the shell-menu.py directory.
    The second one can be saved in any directory of the system where the user that
    will execute the shell-menu.py has the read rights.

    First configuration file is the main one, and the name must be "shell-menu.json".
    The user is free to choose a name for the second one.

Synopsis:
    If all cofigurations have been done correctly just execute

    ./shell-menu.py

    Into the directoy where the program has been installed.

Todo:
    * Same configuration for many hostnames and users with the '*' marker
    * Multiple columns menus based on fixed line number

Changelog:
    05-Sep-2017 : born of the project
    08-Sep-2017 : first realese completed (v1.0)

Author:
    Giuseppe Biolo  < giuseppe.biolo@gmail.com > < https://github.com/gbiolo >

License:
    Copyright (c) 2017 Giuseppe Biolo

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
'''


import json
from socket import gethostname
from getpass import getuser
from subprocess import call
import sys
import termios
import os


def format_string( unformatted, length, allign="sx" ):
    '''Function to format a string to a given length and allignment
    Input parameters are the following:
        input  : string to format
        length : final length of the formatted string; in case of input string
                 longer than the final length, the input string won't be change,
                 and the final string will be the same of the input one
        alling : allignment of the final string; the allowed values are:
                   - sx     : left allignment
                   - dx     : right allignment
                   - center : centred string
                 default value of the parameter "allign" is "sx" (left allignment)
    Return value is the formatted string.
    '''
    if len( unformatted ) >= length:
        return unformatted
    formatted = ""
    spaces = ( length - len(unformatted) )
    if allign == "sx":
        formatted = ( unformatted + (' ' * spaces) )
    elif allign == "dx":
        formatted = ( (' ' * spaces) + unformatted )
    elif allign == "center":
        spaces_sx = int( spaces / 2 )
        spaces_dx = ( int( spaces / 2 ) + ( spaces % 2 ) )
        formatted = ( (' ' * spaces_sx) + unformatted + (' ' * spaces_dx) )
    return formatted


def create_menu( menu ):
    '''Create the grid to show a menu
    A shell-menu output is composed of one or more menu grid.
    Input parameters are:
        menu : a dictionary estracted from the user menu configuration JSON
    The returned value is a dictionary with the following 4 keys:
        rows    : array containing the rows that compose the grid, with header and
                  footer
        size    : width of the grid expressed in character
        links   : dictionary containing the list of the external command of the
                  menu; keys are the menu index, values are external command as
                  indicated in the menu configuration JSON file
    '''
    menu_specs = { "rows" : [], "size" : 0, "links" : {} }
    name = menu["name"]
    scripts = menu["scripts"]
    num_scripts = len( scripts )
    # External command index string maximum length
    index_length = 1
    while num_scripts >= 10:
        index_length += 1
        num_scripts = int(num_scripts / 10)
    # Grid size, calculated on length of menu name and on length of all scripts
    # name
    header_length = len( name ) + 4
    for script in scripts:
        script_length = ( len( script["name"] ) + index_length + 4 )
        if script_length > header_length:
            header_length = script_length
    menu_specs["size"] = (header_length + 3)
    # Create all menu rows that will be inserted into the array 'rows'
    menu_specs["rows"].append( "+-" + ('-'*header_length) + "+" )
    menu_specs["rows"].append( "| " + format_string(name, header_length,
                               "center") + "|" )
    menu_specs["rows"].append( "+-" + ('-'*header_length) + "+" )
    index = int( menu["base"], base=10 )
    for script in scripts:
        index_str = format_string(str(index), index_length, "dx")
        menu_specs["rows"].append( "| "+ format_string( index_str + ") " +
                                   script["name"] + " ", header_length, "sx") + '|' )
        menu_specs["links"][str(index)] = script["script"]
        index += 1
    menu_specs["rows"].append( "+-" + ('-'*header_length) + "+" )
    return menu_specs


# Main program
if __name__ == "__main__":
    hostname = gethostname()
    user = getuser()
    main_conf = None
    menu_conf = None
    # Open and load the main configuration JSON
    with open( os.getcwd()+"/shell-menu.json", "r" ) as configuration:
        main_conf = json.load( configuration )
    with open( main_conf["configurations"][ hostname ][ user ] ) as configuration:
        menu_conf = json.load( configuration )
    vmargin = int( main_conf[ "vmargin" ], base=10 )
    hmargin = int( main_conf[ "hmargin" ], base=10 )
    hpadding = int( main_conf[ "hpadding" ], base=10 )
    while True:
        call( "clear" )
        print( ("\n"*vmargin) + (' '*hmargin) + menu_conf["title"], end="\n\n" )
        menus = []
        for menu in sorted( menu_conf["menus"].keys() ):
            menus.append( create_menu( menu_conf["menus"][menu] ) )
        completed = 0
        while completed < len( menus ):
            print( ' '*hmargin, end='' )
            for menu in menus:
                if len( menu["rows"] ) > 0:
                    print( menu["rows"].pop(0), end=(' '*hpadding) )
                    if len( menu["rows"] ) == 0:
                        completed += 1
                else:
                    print( ' ' * menu["size"], end=(' '*hpadding) )
            print()
        print()
        choice = input( (' '*hmargin) + main_conf["messages"]["choice"] )
        if choice == main_conf["exit_key"]:
            call( "clear" )
            exit()
        else:
            found = 0
            for menu in menus:
                if choice in menu["links"]:
                    found = 1
                    call( "clear" )
                    call( menu["links"][choice] )
                    print()
                    print( (' '*hmargin) + "--------------------" )
                    print( (' '*hmargin) + main_conf["messages"]["completed"], end="\n" )
            if not found:
                print()
                print( (' '*hmargin) + main_conf["messages"]["wrong"], end="\n" )
            # Print the 'back' message in the main JSON configuration file, and
            # wait till the user press the ENTER button to continue
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            new = termios.tcgetattr(fd)
            new[3] = new[3] & ~termios.ECHO
            try:
                termios.tcsetattr(fd, termios.TCSADRAIN, new)
                input( (' '*hmargin) + main_conf["messages"]["back"] )
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
