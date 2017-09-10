## shell-menu is a simple menu for Unix-like systems (Linux/HP-UX/SunOS/etc)

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

### Todo

Minor features are in development stage. These are some of them:
- Same configuration for many hostnames and users with the '*' marker
- Multiple columns menus based on fixed line number

### Changelog

1. (05-Sep-2017) : born of the project
2. (08-Sep-2017) : first realese completed (v1.0)

### Author
Giuseppe Biolo - [send me an email](giuseppe.biolo@gmail.com)

### License
This software is licensed under MIT license.
Copyright (c) 2017 Giuseppe Biolo
