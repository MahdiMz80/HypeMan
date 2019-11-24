@echo off
echo %1
REM call C:\Users\DCSAdmin\Anaconda3\Scripts\activate.bat C:\Users\DCSAdmin\Anaconda3
REM call C:\Users\reso\Anaconda3\pkgs\conda-4.7.10-py37_0\Scripts\activate.bat C:\Users\reso\Anaconda3
rem call C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3
call C:\Users\jow\Anaconda3\Scripts\activate.bat C:\Users\jow\Anaconda3
python gsheet_upload.py %1