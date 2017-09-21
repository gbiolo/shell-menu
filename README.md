## shell-menu is a simplified menu for shell environment


### Description

The main target of the project is to provide an easy to deploy menu to use in
shell mode, for example in case of remote SSH connection, that allow the user
to easily execute a set of command.

The configuration is based on two JSON format files. The first must be located
in a subdirectory called 'cnf' inside the shell-menu.py directory.
The second one can be saved in any directory of the system where the user that
will execute the shell-menu.py has the read grants.

First configuration file is the main one, and the name must be "shell-menu.json".
The user is free to choose a name for the second one.


### Synopsis

If all cofigurations have been done correctly just execute

```markdown
./shell-menu.py
```

Into the directoy where the program has been installed.


### Requirements

First of all it can be used only in an Unix-like operating system
(Linux, Solaris, HP-UX, ecc.).

For Python interpreter, you need at least Python 2.6+ or Python 3.3+. With
older versions the program won't run due the import of the __future__.

By default the environment used to execute the program is Python 3, but you can
change it just replacing "python3" with "python" or "python2" (depending your system
environment) into the first line (hash-bang) of the "sheel-menu.py".


### Todo

Minor features are in development stage. These are some of them:
- Multiple columns menus based on fixed line number


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
