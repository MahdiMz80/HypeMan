@echo off

REM (TODO INSERT DOCUMENTATION LINK HERE....)
REM Set the python variables for your system here.
REM 
REM PYTHON_ACTIVATE
REM activate.bat is the bat file that starts your python environment
REM Anaconda Default: %USERPROFILE%\Anaconda3\Scripts\activate.bat
REM          Example: C:\Users\tony\anaconda3\Scripts
REM
REM HYPEMAN_FOLDER
REM This is the folder that you've installed HypeMan
REM Default C:\HypeMan
REM
REM PYTHON_ENVIRONMENT
REM This is the name of the python environment that you want to run.
REM To use the default environment just leave it blank.  
REM Best practice is to create a dedicated hypeman python environment

set PYTHON_ACTIVATE=C:\Users\tony\anaconda3\Scripts\activate.bat
set HYPEMAN_FOLDER=C:\HypeMan
set PYTHON_ENVIRONMENT=hypeman

REM run the hypeman listener python script
REM call %PYTHON_FOLDER%.\activate.bat %PYTHON_ENVIRONMENT%
echo PYTHON_ACTIVATE: %PYTHON_ACTIVATE%
echo HYPEMAN_FOLDER: %HYPEMAN_FOLDER%
echo PYTHON_ENVIRONMENT: %PYTHON_ENVIRONMENT%

call %PYTHON_ACTIVATE% %PYTHON_ENVIRONMENT%
python hypeman_listener.py