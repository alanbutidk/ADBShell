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

## NOTICE
For this to work, you'll need the entire Android Debug Bridge installation (including adb, .dlls, fastboot, hw etc...).
As this uses: ```__file__``` inside the code.

*(No Amount of adb-shell library functions were used)*

### Something else
If you see no downloads, it means. __*uhhhhhhhhhhhh*__, i havent made the zip (it contains ADB, Fastboot, Compiled and Interpreted versions of the Shell.

(COMPILED VIA _Official CPython/Cython_ for static, _PyInstaller_ for dynamic builds)
