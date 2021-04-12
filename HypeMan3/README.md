# HYPEMAN 3: THE HYPENING
HypeMan 3 is a rewrite of the HypeMan discord bot from lua to Python.

## Wait, why?
HypeMan was originally written in lua using the [Discordia](https://github.com/SinisterRectus/Discordia "Discordia") lua discord library, and ran in the [luvit](https://luvit.io/) lua repl environment.  At the time it was thought that having the bot written in lua, the same language used in the DCS mission environment, would be handy.  More functionality was added over time, and most of that functionality was implemented with python scripts.  The lua bot called the python functions through windows BAT files which would setup the python environment properly: each new python function would have a .bat file wrapper that would pass command line arguments.  Output was handled by the python code writing files with fixed file names.

The goal of a python re-write is to avoid having to write .bat file wrappers for each new python script, make it easy to add and execute new feature of functions in python, and hopefully make it easier for others to add new functionality and extend the bot to react to different messages or events in Discord or DCS.


## Installation

### Configuration File
The configuration is held in `hypeman.ini`  which is **not** tracked in the repository.  You must take the  `example.ini` copy/rename it to **hypeman.ini** and edit the values in the file to suit your needs.

**Example hypeman.ini**:

```
[HYPEMAN]
BOT_ID = AIzOTE2NjQ9MjQ0MTkyNzc1.Xa1S2w.HyOjhZk7PcFyUGMuplLtqG3khiI
PORT = 10081
HOST = localhost
```

### Python Bat File Launcher

Copy/rename `run_hypeman_example.bat` file to `run_hypeman.bat`, and edit the location of the variables to activate your python distribution.  An easy way to get this is to look at any shortcut in the Start Menu that starts your python environment and look for the path to `activate.bat`.

Example `run_hypeman.bat`:
```
@echo off
set PYTHON_ACTIVATE=C:\Users\tony\anaconda3\Scripts\activate.bat
set PYTHON_ENVIRONMENT=hypeman

call %PYTHON_ACTIVATE% %PYTHON_ENVIRONMENT%
python hypeman_listener.py
```

#### Environment variables set in the BAT file:

* `PYTHON_ACTIVATE` - This specifies the location of a bat file that activates and sets up your python environment.  For the Anaconda Python distribution this is called `activate.bat` and it usually lives in your `%USERPROFILE%\anaconda3\Scripts\` directory.
* `PYTHON_ENVIRONMENT` - This specifies the name of the python virtual environment (venv) that the HypeMan bot will run in.  See the code examples below for instructions on how to create and activate a python environment.  Leave this empty and it will run in the default/main environment


## Python Environment
Starting with HypeMan 3 we will try to encourage people to setup a python virtual environment (venv) for hypeman.  Here are some rough commands to first list your python environment, update, and create the hypeman environment.  Notice that discord.py is installed with pip not conda.

```bash
conda info --envs
conda update --all
conda update conda
conda create -n hypeman
conda activate hypeman
pip install -U discord.py
```



# TODO and outstanding issues
1.) Make instructions for both Anaconda Python and the python.org release (including the py.exe launcher?)

2.) Find the right code/plugin structure to allow easy extensibility of the Discord bot

3.) Finish TODO list

