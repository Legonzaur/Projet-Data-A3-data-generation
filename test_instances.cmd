@echo off

:loop
python vrp_test.py

if %ERRORLEVEL% EQU 0 (
   goto loop
) else (
   echo Failure Reason Given is %errorlevel%
   pause
   exit /b %errorlevel%
)

