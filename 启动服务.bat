@echo off

set DJANGO_APP_DIR=./django_app

REM Change directory to the django_app directory
cd %DJANGO_APP_DIR%

REM Activate the ML virtual environment
call conda activate ML >nul 2>&1
if %errorlevel% neq 0 (
    echo Error activating virtual environment. Please check if Conda is installed.& pause & exit /b 1
)

REM Run the Django server and display the output in the terminal
python manage.py runserver

REM Prompt user to close window when finished
echo Press any key to close this window.
pause >nul

REM Release the port occupied by the server (optional, depends on the Django configuration)
REM Replace '8000' with the actual port number used by your Django server
taskkill /F /PID $(for /f "tokens=5" %%i in ('netstat -aon ^| findstr :8000') do @echo %%i)
