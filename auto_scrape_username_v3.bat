@echo off
setlocal EnableDelayedExpansion
REM Instagram Auto Scraper - Username Input Version (Simplified)
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

REM Step 2: Extract video URLs to a clean list
cd /d "C:\Users\alvin\Desktop\ig_Scraper"

echo.
echo Step 2: Extracting video URLs...
echo Step 2: Extracting video URLs... >> %LOGFILE%

REM Create a clean URLs file with only reel/video links (get most recent ones first)
powershell -Command "Get-Content 'C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts_%USERNAME%.txt' | Where-Object {$_ -match 'https://www\.instagram\.com/[^/\s]+/(reel|tv)/[^/\s]+'} | ForEach-Object {if($_ -match '(https://www\.instagram\.com/[^/\s]+/(reel|tv)/[A-Za-z0-9_-]+)'){$matches[1].Split('?')[0]}} | Select-Object -Unique | Select-Object -First 10" > video_urls_%USERNAME%.txt

REM Debug: Show what URLs we found
echo Debug: Found video URLs:
type video_urls_%USERNAME%.txt
echo.

REM Step 3: Process each URL
set COUNTER=1
for /f "usebackq delims=" %%i in (video_urls_%USERNAME%.txt) do (
    echo.
    echo ==============================================
    echo Running scraper !COUNTER! for: %%i
    echo ==============================================
    echo Running scraper !COUNTER! for: %%i >> %LOGFILE%
    
    REM Double-check the URL before running
    echo Debug: About to run: python main_scraper.py "%%i" 30 "%USERNAME%_!COUNTER!"
    
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
    
    REM Add a small delay between runs
    timeout /t 2 /nobreak > nul
)

REM Clean up temp files
del "C:\Users\alvin\Desktop\InstagramPrivSniffer\temp_posts_%USERNAME%.txt" 2>nul
del "video_urls_%USERNAME%.txt" 2>nul

echo.
echo ========================================
echo All posts processed for %USERNAME%!
echo Total videos processed: !COUNTER!
echo ========================================
echo ======================================== >> %LOGFILE%
echo All posts processed for %USERNAME%! >> %LOGFILE%
echo Total videos processed: !COUNTER! >> %LOGFILE%
echo Completed at %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Log saved to: %LOGFILE%
pause