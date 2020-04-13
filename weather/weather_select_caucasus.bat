: weather_select.bat - pops up a dialog to select a mission then modifies the weather
: based on the Sochi or Batumi weather stations from checkwx.com
: originally created by the Havov-company.com DCS group
:
: example launch file for DCS used with dcs_weather.py
: by havoc-company.com
: you need python 3 (and requests module for python - pip install requests in dos to install) 
: and 7z installed on server hosting PC
: you will need to edit this file to change parameters to match your install
: contact HC_Official in ED forums for any queries
: V 1.0.3
: try NOT to use paths with spaces in them, it is a fecking ballache

@echo off
setlocal

: EDIT THIS TO MATCH THE PATH TO YOUR PYTHON ENVIRONMENT ACTIVATION SCRIPT
call D:\Anaconda3\Scripts\activate.bat D:\Anaconda3

: settings for dcs_weather.py - airports weather to query
SET PRIMARY_AIRPORT=URSS 
SET BACKUP_AIRPORT=UGSB

: edit below this to point to where your python exe is
SET PYTHON_EXE="python"

: you want to use current realtime on server ?  Note this has been disabled
SET TIME_CONTROL=real

: set this to where your 7z.exe is installed
SET zip="D:\Program Files\7-Zip\7z.exe"

: where you store your mission miz files
:SET MISSION_PATH=C:\Users\reso\Saved Games\DCS.openbeta\Missions\weather\

: mission name minus the file extension

@echo off
set dialog="about:<input type=file id=FILE><script>FILE.click();new ActiveXObject
set dialog=%dialog%('Scripting.FileSystemObject').GetStandardStream(1).WriteLine(FILE.value);
set dialog=%dialog%close();resizeTo(0,0);</script>"

for /f "tokens=* delims=" %%p in ('mshta.exe %dialog%') do set "file=%%p"
echo selected  file is : "%file%"

FOR %%i IN ("%file%") DO (
ECHO filedrive=%%~di
ECHO filepath=%%~pi
ECHO filename=%%~ni
ECHO fileextension=%%~xi

SET MISSION_NAME=%%~ni
SET MISSION_PATH=%%~pi
)

echo %MISSION_NAME%
echo %MISSION_PATH%

: SET MISSION_NAME=weather


SET MISSION="%MISSION_PATH%%MISSION_NAME%.miz"

: path and name of weather python script
SET PYTHON_SCRIPT="C:\HypeMan\weather\dcs_weather.py"


SET TEST=%time:~0,1%
SET HOUR=%time:~0,2%
IF  "%TEST%" == " "  SET HOUR=%time:~1,1%


: this override was added so that if it is too late in the year (dark a lot in evenings) then people would get some time were it is light for a bit
: IF %HOUR% GEQ 18 SET TIME_CONTROL=6
@echo %TIME_CONTROL%


cd /D %MISSION_PATH%
%PYTHON_EXE% %PYTHON_SCRIPT% %MISSION% %PRIMARY_AIRPORT% %BACKUP_AIRPORT% %TIME_CONTROL%

: rename .miz to .zip because 7z don't like miz file extension
ren %MISSION_NAME%.miz %MISSION_NAME%.zip

: add the updated mission to the zip file
%zip% a -tzip %MISSION_NAME%.zip mission -mx9 

: rename it back to miz
ren %MISSION_NAME%.zip %MISSION_NAME%.miz 


: cd /D %DCS_PATH%
: start /D%DCS_PATH% /B dcs.exe


: pause

: end Batch portion / begin PowerShell hybrid chimera #>


