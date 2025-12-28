@echo off
TITLE Project Setup - DevOps Task

echo.
echo [1/4] Installing Python Dependencies...
pip install pandas pymongo
IF %ERRORLEVEL% NEQ 0 (
    echo Error installing python libraries. Please ensure Python and Pip are in your PATH.
    pause
    exit /b
)

echo.
echo [2/4] Setting up MongoDB Portable...
python setup_mongo.py
IF %ERRORLEVEL% NEQ 0 (
    echo Error running setup script.
    pause
    exit /b
)

echo.
echo [3/4] Starting MongoDB Server...
if not exist "mongodb\bin\mongod.exe" (
    echo MongoDB executable not found at mongodb\bin\mongod.exe
    pause
    exit /b
)

echo Starting MongoDB in a new window...
start "MongoDB Server" cmd /k ".\mongodb\bin\mongod.exe --dbpath .\mongodb_data --bind_ip 127.0.0.1"

echo Waiting for MongoDB to initialize (5 seconds)...
timeout /t 5 /nobreak >nul

echo.
echo [4/4] Setup Complete!
echo.
echo You can now run the tasks. The results will be saved in the 'Results' folder.
echo   To run Task 1: python task1_pipeline.py
echo   To run Task 2: python task2_analysis.py
echo.
pause
