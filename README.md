# ADBShell

ADBShell is a shell wrapper written in __Python 3.13__. This *Shell Wrapper* works by taking inputs (hardcoded, case-sensitive) and executing specific commands, using the subprocess library, pathlib library, platform library, and the __*average snake standard library*__.

## About files

*shell.c* is the Cython translation to the shell.py done on a Windows x86_64 Host

*shell.py* is the orignal python file which contains the orignal code of the shell

## Libraries Used

Libraries used in the file:

```import subprocess as s```

```from pathlib import Path```

```import platform```

```import os```

```from concurrent.futures import ThreadPoolExecutor```

## Installing

To install, choose your desired flavour while downloading: the full .zip or the standalone .exe of the shell, the .py version of the shell or the Cython .c version of the shell.

_*If you choose .zip*_: 

Extract the zip to anywhere on your PC, examples: C:\Users\MyUser\Downloads\ADBShell_OSTYPE_FOR_.zip -> C:\Users\MyUser\

or

/root/MyDownloads/ADBShell_OSTYPE_FOR_.zip -> /root/MyDownloads/ADBShell/

You can extract the zip by many popular programs like:

*WinRAR* -> Supports ZIP and RAR formats; Free+Classic

*7Zip* -> ZIP, ISO formats; Open-Source+Free+Classic

Now, you can either add it to your Path or directly launch cmd.exe at the location; both are fine.

To add it to your PATH:

*Windows*:
Open _View Advanced System Settings_ window, Click on "Environment Variables", User variables for MyUser (Example user name), Click on the PATH One under the text

Click on New, Put the PATH where the folder exists (Example: C:\Users\MyUsers\Downloads\ADBShell), Press enter and OK, OK, OK on all windows.

Now you can call it from anywhere you want (adb.exe & fastboot.exe)

OR

Open a CMD Window at the Folders Path
and "python.exe shell.py" OR "ADBShell.exe"

*Linux*:

Enter "echo $0" in your terminal to find out your terminal:

*If it is _Bash_*:

Use Vim or GNU Nano to open up this exact path: "nano ~/.bashrc" or "vim ~./bashrc"

Go to the bottom and enter this line:

*export PATH="$PATH:/your/shell/path/"*

where "/your/shell/path" is the full path to the Folder that contains the binaries

and Exit the editor after saving (Nano: ctrl+s; ctrl+x, Vim: esc; :wq)

*If it is _Zsh_*:

Open up ~/.zshrc
and do the same as bash

*_If it is a executable/.py file_*: Place it somewhere
