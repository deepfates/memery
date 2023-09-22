@echo off
setlocal enabledelayedexpansion

:: Display warning message
echo This uninstalls *** ALL *** python libraries so you can try the install script again.
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
            goto cleanup
        )
    )
    
    pip uninstall -r installed_packages.txt -y
) else (
    echo Exiting...
    goto end
)

:cleanup
:: Clean up
if exist installed_packages.txt del installed_packages.txt

:end
:: End of script
endlocal
