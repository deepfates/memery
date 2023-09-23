@echo off
setlocal enabledelayedexpansion

:: Display warning message
echo WARNING this uninstalls *** ALL *** python libraries
echo WARNING this deletes the poetry.lock file
echo Are you sure you want to continue? y/N
set /p user_input=

:: Check user input
if /i "%user_input%"=="y" (
    echo Uninstalling Python libraries...
    pip freeze > installed_packages.txt
    
    :: Check if installed_packages.txt is empty
    for %%A in (installed_packages.txt) do (
        if %%~zA==0 (
            echo all pip packages uninstalled
            goto poetry_check
        )
    )
    
    pip uninstall -r installed_packages.txt -y
    goto poetry_check
) else (
    echo Exiting...
    goto end
)

:poetry_check
:: Check if poetry is installed
poetry -V >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Poetry is installed, removing all environments...
    for /f "delims=" %%i in ('poetry env list') do poetry env remove %%i
) else (
    echo Poetry is not installed, skipping poetry environment removal.
)

:cleanup
:: Clean up
if exist installed_packages.txt del installed_packages.txt

:: Delete poetry.lock if it exists
if exist poetry.lock del poetry.lock

:end
:: End of script
endlocal
