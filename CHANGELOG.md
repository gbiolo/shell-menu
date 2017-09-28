# Changelog
All notable changes to this project will be documented in this file.

___
#### 2017-09-05
Born of the project

___
#### 2017-09-08
First release with the principal functions implemented

___
#### 2017-09-11
##### Added
* Use of the same configuration JSON for many hostnames and users using the '*'
  marker

___
#### 2017-09-21
##### Added
* Project totally redesigned using objects
* Info box with auto-split text and multi text
##### Removed
* Customizable text for interface (english is enought)

___
#### 2017-09-22
##### Added
* Interactive installer with Python interpreter recognition

___
#### 2017-09-27
##### Added
* Use of environment variables into commands path of the user configuration JSON,
  indicated as usual with a "$" followed by the variable name
* If no info box is present in the menu, the user doesn't insert an empty "info"
  key in the configuration file

___
#### 2017-09-28
##### Added
* Use of environment variables into main configuration JSON file paths
* User exit sequence and style configurations are optional now; if one or more
  values are not present, they will be set to a built-in default value
