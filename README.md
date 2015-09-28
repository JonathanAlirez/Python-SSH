# Python-SSH
A simple Python script, using Paramiko, to use ssh commands

#Uses
Using this Python script, you can SSH into any server and run commands through the command-line interface.
This script uses Paramiko, a SSH Library to allow for this connection, so you need to have it installed to
be able to take advantage of this SSH Script.

#Dependencies
Make sure to have Paramiko installed, a simple
```
pip install paramiko
```
should do.

#Drawbacks
Currently there is no way to interact with any command-line interface programs, such as emacs or vim.
So you can do all your SSH work through this program, but will not be able to use these programs.
All other commands are supported.
