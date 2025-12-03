@echo off
REM Instagram Auto Scraper - Username Input Version
REM This script asks for a username, uses InstagramPrivSniffer to get posts, then scrapes them

REM Activate conda environment
echo Activating conda environment...
call conda activate 11_10_scraper
if errorlevel 1 (
    echo Failed to activate conda environment. Make sure conda is installed and in PATH.
    pause
    exit /b 1
)

REM Get username from user
echo ========================================
echo Instagram Auto Scraper - Username Mode
echo ========================================
echo.
set /p USERNAME="Enter Instagram username (without @): "

if "%USERNAME%"=="" (
    echo Error: No username provided.
    pause
    exit /b 1
)

echo.
echo Target username: %USERNAME%
echo.

REM Set up logging
set LOGFILE=auto_scrape_%USERNAME%_log.txt
echo. > %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Instagram Auto Scraper - Username: %USERNAME% >> %LOGFILE%
echo Started at %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%

REM Step 1: Use InstagramPrivSniffer to get post links
echo Step 1: Fetching post links for %USERNAME%...
echo Step 1: Fetching post links for %USERNAME%... >> %LOGFILE%

cd /d "C:\Users\alvin\Desktop\InstagramPrivSniffer"
python main.py --name %USERNAME% > temp_posts.txt 2>&1

if errorlevel 1 (
    echo Error: Failed to fetch posts from InstagramPrivSniffer
    echo Error: Failed to fetch posts from InstagramPrivSniffer >> %LOGFILE%
    pause
    exit /b 1
)

REM Step 2: Extract URLs from the output and run scraper
cd /d "C:\Users\alvin\Desktop\ig_Scraper"

echo.
echo Step 2: Processing found posts...
echo Step 2: Processing found posts... >> %LOGFILE%

REM Parse the temp file and extract Instagram URLs
set COUNTER=1

REM Debug: Show what we found in the temp file
echo Debug: Contents of temp_posts.txt:
type "C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts.txt"
echo.
echo Debug: Searching for Instagram URLs...

for /f "tokens=*" %%i in ('findstr /i "https://www.instagram.com/" "C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts.txt"') do (
    echo Debug: Found line: %%i
    set "URL=%%i"
    call :process_url
)

REM Clean up temp file
del "C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts.txt" 2>nul

echo.
echo ========================================
echo All posts processed for %USERNAME%!
echo ========================================
echo ======================================== >> %LOGFILE%
echo All posts processed for %USERNAME%! >> %LOGFILE%
echo Completed at %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Log saved to: %LOGFILE%
pause
goto :eof

:process_url
echo Debug: Processing URL: %URL%

REM Extract clean URL by looking for https://www.instagram.com/ pattern
REM Use a more robust approach - find all tokens and look for the Instagram URL
set "CLEAN_URL="

REM Parse all tokens in the line to find the Instagram URL
for %%t in (%URL%) do (
    set "TOKEN=%%t"
    call :check_token
)

if defined CLEAN_URL (
    echo Debug: Successfully extracted URL: %CLEAN_URL%
    goto :run_scraper
) else (
    echo Debug: Could not extract URL from: %URL%
)
goto :eof

:check_token
REM Check if this token is an Instagram URL
echo %TOKEN% | findstr /b "https://www.instagram.com/" >nul
if not errorlevel 1 (
    set "CLEAN_URL=%TOKEN%"
)
goto :eof

:run_scraper
echo.
echo Running scraper %COUNTER% for: %CLEAN_URL%
echo Running scraper %COUNTER% for: %CLEAN_URL% >> %LOGFILE%

REM Run the scraper with 30 scrolls and auto-generated filename
python main_scraper.py "%CLEAN_URL%" 30 "%USERNAME%_%COUNTER%"

if errorlevel 1 (
    echo Warning: Scraper %COUNTER% failed for %CLEAN_URL%
    echo Warning: Scraper %COUNTER% failed for %CLEAN_URL% >> %LOGFILE%
) else (
    echo Successfully completed scraper %COUNTER%
    echo Successfully completed scraper %COUNTER% >> %LOGFILE%
)

echo. >> %LOGFILE%
set /a COUNTER+=1
goto :eof