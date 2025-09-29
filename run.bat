@echo off
REM Go to project directory (optional)
cd /d %~dp0

REM Activate the virtual environment
call myenv\Scripts\activate.bat

REM Run your Python script inside the venv
python main.py

REM Pause so you can see any errors before window closes
pause