@echo off
REM Check if Python is installed and in PATH
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    exit /b 1
)

REM Install Python dependencies from requirements.txt
pip install -r ./install/requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies from requirements.txt.
    exit /b 1
)

REM Check if Poetry is installed and in PATH
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo Poetry is not installed or not in PATH.
    exit /b 1
)

REM Run 'poetry install' to install dependencies via Poetry
poetry install
if %errorlevel% neq 0 (
    echo Failed to install Python dependencies via Poetry.
    exit /b 1
)

REM Use local build folder
echo Use local build folder
pip install -e .

REM Run the Python script
python ./install/windows-install.py

REM Check the exit code of the Python script
if %errorlevel% neq 0 (
    echo Failed to execute Python script.
    exit /b 1
)
echo Successfully executed Python script.
