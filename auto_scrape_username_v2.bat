@echo off
setlocal EnableDelayedExpansion
REM Instagram Auto Scraper - Username Input Version (Improved)
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
python main.py --name %USERNAME% > temp_posts_%USERNAME%.txt 2>&1

if errorlevel 1 (
    echo Error: Failed to fetch posts from InstagramPrivSniffer
    echo Error: Failed to fetch posts from InstagramPrivSniffer >> %LOGFILE%
    pause
    exit /b 1
)

REM Step 2: Extract URLs using PowerShell and run scraper
cd /d "C:\Users\alvin\Desktop\ig_Scraper"

echo.
echo Step 2: Processing found posts...
echo Step 2: Processing found posts... >> %LOGFILE%

REM Extract URLs and run scrapers with conda environment - VIDEOS ONLY
set COUNTER=1
for /f "usebackq delims=" %%i in (`powershell -Command "Get-Content 'C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts_%USERNAME%.txt' | Where-Object {$_ -match 'https://www\.instagram\.com/[^\s]+/(reel|tv)/'} | ForEach-Object {if($_ -match 'https://www\.instagram\.com/[^\s]+/(reel|tv)/[^/\s]+'){$matches[0]}}"`) do (
    echo.
    echo Running scraper !COUNTER! for: %%i
    echo Running scraper !COUNTER! for: %%i >> %LOGFILE%
    
    call conda activate 11_10_scraper
    python main_scraper.py "%%i" 30 "%USERNAME%_!COUNTER!"
    
    if errorlevel 1 (
        echo Warning: Scraper !COUNTER! failed for %%i
        echo Warning: Scraper !COUNTER! failed for %%i >> %LOGFILE%
    ) else (
        echo Successfully completed scraper !COUNTER!
        echo Successfully completed scraper !COUNTER! >> %LOGFILE%
    )
    
    echo. >> %LOGFILE%
    set /a COUNTER+=1
)

REM Clean up temp file
del "C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts_%USERNAME%.txt" 2>nul

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