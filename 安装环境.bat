@echo off

set REQUIREMENTS_PATH=./django_app/requirements.txt

REM Check if Conda is installed
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo Conda not found. Please install Conda and ensure that PATH is correctly configured.& pause & exit /b 1
)

REM Check if a virtual environment named "ML" already exists
call conda activate ML >nul 2>&1
if %errorlevel% equ 0 (
    echo Virtual environment 'ML' already exists. Skipping creation step.
) else (
    echo Creating virtual environment...
    conda create -n ML python=3.10 -y >nul 2>&1
    if %errorlevel% neq 0 (
        echo Error creating virtual environment. Please check if Python 3.10 is installed.& pause & exit /b 1
    )
    echo Virtual environment created.
)

REM Install dependencies
echo Installing dependencies...
call conda activate ML >nul 2>&1
if %errorlevel% neq 0 (
    echo Error activating virtual environment. Please check if Conda is installed.& pause & exit /b 1
)
pip install -r %REQUIREMENTS_PATH%
if %errorlevel% neq 0 (
    echo Error installing dependencies. Please check if requirements.txt file exists.& pause & exit /b 1
)
echo Dependencies installed.

REM Prompt user to close window when finished
echo Press any key to close this window.
pause >nul
