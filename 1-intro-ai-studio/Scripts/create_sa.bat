@echo on
setlocal enabledelayedexpansion

REM ============================================
REM Yandex Cloud Service Account Setup Script
REM Creates SA with ai.editor role and .env file
REM ============================================

set SA_NAME=ai-studio-sa
set ENV_FILE=.env

echo === Yandex Cloud Service Account Setup ===
echo.

REM Check if yc CLI is installed
where yc >nul 2>&1
if errorlevel 1 (
    echo ERROR: Yandex Cloud CLI yc is not installed or not in PATH
    echo Install it from: https://cloud.yandex.ru/docs/cli/quickstart
    exit /b 1
)

REM Get current folder_id
echo Getting folder_id...
for /f "tokens=*" %%i in ('yc config get folder-id 2^>nul') do set FOLDER_ID=%%i

if "%FOLDER_ID%"=="" (
    echo ERROR: folder-id is not configured in yc CLI
    echo Run: yc init
    exit /b 1
)
echo Folder ID: %FOLDER_ID%

REM Check if service account already exists
echo.
echo Checking if service account "%SA_NAME%" exists...
for /f "tokens=*" %%i in ('yc iam service-account get --name %SA_NAME% --format json 2^>nul ^| findstr /c:"id"') do set SA_EXISTS=1

if defined SA_EXISTS (
    echo Service account already exists. Getting its ID...
    for /f "tokens=*" %%i in ('yc iam service-account get --name %SA_NAME% --format json ^| findstr /c:"id" ^| for /f "tokens=2 delims=:," %%a in ^('findstr /c:"id"'^) do @echo %%~a') do set SA_ID=%%i
) else (
    echo Creating service account "%SA_NAME%"...
    for /f "tokens=2 delims=: " %%i in ('yc iam service-account create --name %SA_NAME% --format json ^| findstr /c:"\"id\""') do set SA_ID=%%~i
)

REM Get service account ID properly
for /f "delims=" %%i in ('yc iam service-account get --name %SA_NAME% --format json 2^>nul') do set SA_JSON=%%i
for /f "tokens=2 delims=:, " %%i in ('yc iam service-account get --name %SA_NAME% 2^>nul ^| findstr /c:"id:"') do set SA_ID=%%i

if "%SA_ID%"=="" (
    echo ERROR: Failed to get service account ID
    exit /b 1
)
echo Service Account ID: %SA_ID%

REM Assign ai.editor role
echo.
echo Assigning ai.editor role to the service account...
yc resource-manager folder add-access-binding --id %FOLDER_ID% --role ai.editor --subject serviceAccount:%SA_ID% >nul 2>&1
if errorlevel 1 (
    echo Warning: Role might already be assigned or insufficient permissions
) else (
    echo Role ai.editor assigned successfully
)

REM Create API key
echo.
echo Creating API key...
for /f "tokens=2 delims=: " %%i in ('yc iam api-key create --service-account-name %SA_NAME% 2^>nul ^| findstr /c:"secret:"') do set API_KEY=%%i

if "%API_KEY%"=="" (
    echo ERROR: Failed to create API key
    exit /b 1
)
echo API key created successfully

REM Create .env file
echo.
echo Creating %ENV_FILE% file...
(
    echo folder_id=%FOLDER_ID%
    echo api_key=%API_KEY%
) > %ENV_FILE%

echo.
echo === Setup Complete ===
echo.
echo Created %ENV_FILE% with:
echo   - folder_id=%FOLDER_ID%
echo   - api_key=***hidden***
echo.
echo Service account "%SA_NAME%" is ready to use.

endlocal
