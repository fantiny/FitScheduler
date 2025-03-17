@echo off
chcp 65001 >nul
echo Starting BSweetOrder Yoyaku Backend API Service...
echo.

REM ===== Option to skip environment setup =====
set SKIP_ENV_SETUP=0
set CONFIRM_SKIP=n
set /p CONFIRM_SKIP="Do you want to skip environment setup and use your pre-configured environment? (y/n, default: n): "
if /i "%CONFIRM_SKIP%"=="y" set SKIP_ENV_SETUP=1

if %SKIP_ENV_SETUP% EQU 1 (
    REM ===== Use Pre-configured Environment =====
    echo Using pre-configured environment...
    echo Starting backend API service...
    start cmd /k "cd /d %~dp0 && uvicorn main:app --reload --port 8000"
    goto :display_info
)

REM ===== Step 1: Environment Check =====
echo Step 1: Checking Python environment...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.8+ and try again.
    goto :error
)

python -c "import sys; print('Python version: ' + sys.version.split()[0]); sys.exit(0 if int(sys.version.split()[0].split('.')[0]) >= 3 and int(sys.version.split()[0].split('.')[1]) >= 8 else 1)"
if %errorlevel% neq 0 (
    echo [ERROR] Python version is too low. Python 3.8+ is required.
    goto :error
)

REM ===== Step 2: Virtual Environment Check and Setup =====
echo Step 2: Checking virtual environment...
if not exist venv\ (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        goto :error
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists, skipping creation step.
)

REM ===== Step 3: Dependency Check and Installation =====
echo Step 3: Checking dependencies...
set REQUIREMENTS_CHECK=0
venv\Scripts\python -c "try: import fastapi; import sqlalchemy; import pymysql; print('Dependencies already installed'); exit(0)\nexcept ImportError: exit(1)" >nul 2>nul
if %errorlevel% neq 0 (
    set REQUIREMENTS_CHECK=1
)

if %REQUIREMENTS_CHECK% equ 1 (
    echo Installing project dependencies...
    echo Note: Using --only-binary=:all: option to avoid compilation issues
    REM Set Python IO encoding to UTF-8 to resolve encoding issues
    set PYTHONIOENCODING=utf-8
    venv\Scripts\pip install -r requirements.txt --only-binary=:all: -i https://pypi.org/simple/
    if %errorlevel% neq 0 (
        echo [WARNING] Failed to install with binary-only packages. Trying with specific pydantic version...
        venv\Scripts\pip install pydantic==2.4.2 pydantic-core==2.10.1 --only-binary=:all: -i https://pypi.org/simple/
        venv\Scripts\pip install -r requirements.txt --only-binary=:all: -i https://pypi.org/simple/
        if %errorlevel% neq 0 (
            echo [ERROR] Failed to install dependencies.
            goto :error
        )
    )
    echo Dependencies installed successfully.
) else (
    echo Dependencies already installed, skipping installation step.
)

REM ===== Step 4: Start Service with Virtual Environment =====
echo Step 4: Starting backend API service using virtual environment...
start cmd /k "cd /d %~dp0 && venv\Scripts\activate && venv\Scripts\uvicorn main:app --reload --port 8000"

:display_info
echo.
echo Backend API service is starting...
echo The following services will be available in a few seconds:
echo - Backend API: http://localhost:8000
echo - Backend API Documentation: http://localhost:8000/docs
echo.
echo Please do not close this window, closing will terminate the service!
goto :end

:error
echo.
echo An error occurred during startup. Please resolve the above issues and try again.
pause
exit /b 1

:end
pause 