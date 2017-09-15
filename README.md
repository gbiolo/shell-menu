## shell-menu is a simplified menu for shell environment


### Description

The main target of the project is to provide an easy to deploy menu to use in
shell mode, for example in case of remote SSH connection, that allow the user
to easily execute a set of command.

The configuration is based on two JSON format files. The first must be located
in a subdirectory called 'cnf' inside the shell-menu.py directory.
The second one can be saved in any directory of the system where the user that
will execute the shell-menu.py has the read rights.

First configuration file is the main one, and the name must be "shell-menu.json".
The user is free to choose a name for the second one.


### Synopsis

If all cofigurations have been done correctly just execute

```markdown
./shell-menu.py
```

Into the directoy where the program has been installed.


### Requirements

The only requirement of shell-menu is Python 3. The software won't run with older
versions of Python.


### Todo

Minor features are in development stage. These are some of them:
- Multiple columns menus based on fixed line number


### Changelog

1. (05-Sep-2017) : born of the project
2. (08-Sep-2017) : first realese completed (v1.0)
3. (11-Sep-2017) : implemeted the use of the same configuration JSON for many
                   hostnames and users with the '*' marker


### Author

Giuseppe Biolo - giuseppe (dot) biolo (at) gmail (dot) com


### License

This software is licensed under GPL v3 license.

Copyright (c) 2017 Giuseppe Biolo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can read the full text of the GNU General Public License version 3
[here](http://www.gnu.org/licenses/).
