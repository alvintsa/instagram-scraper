@echo off
REM Instagram Scraper - Multiple Commands Runner
REM Edit the URLs and parameters below to customize your runs

REM Activate conda environment (change 'base' to your environment name)
echo Activating conda environment...
call conda activate 11_10_scraper
if errorlevel 1 (
    echo Failed to activate conda environment. Make sure conda is installed and in PATH.
    pause
    exit /b 1
)

set LOGFILE=batch_run_log.txt
echo. > %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Instagram Comment Scraper - Batch Runner >> %LOGFILE%
echo Started at %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo. >> %LOGFILE%

echo ========================================
echo Instagram Comment Scraper - Batch Runner
echo ========================================
echo.

REM Command 1
echo Running Command 1...
echo Running Command 1... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DQNbQ9jEbAb/?igsh=MW9mbDlyMHBrbzJ4dw%3D%3D" 70 aaron_1
echo Finished Command 1
echo Finished Command 1 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 2
echo Running Command 2...
echo Running Command 2... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DPqHlRxjVe8/?igsh=NjFib2hiazh5bWN1" 30 aaron_2
echo Finished Command 2
echo Finished Command 2 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 3
echo Running Command 3...
echo Running Command 3... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DB_lKFPvk5K/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 70 pov_husband_1
echo Finished Command 3
echo Finished Command 3 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 4
echo Running Command 4...
echo Running Command 4... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DB3w1wjPbp7/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 70 pov_husband_2
echo Finished Command 4
echo Finished Command 4 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 5
echo Running Command 5...
echo Running Command 5... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DRDL2yPkodj/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 50 jason_the_ween_1
echo Finished Command 5
echo Finished Command 5 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 6
echo Running Command 6...
echo Running Command 6... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DQ7UboqEmLA/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 50 jason_the_ween_2
echo Finished Command 6
echo Finished Command 6 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 7
echo Running Command 7...
echo Running Command 7... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DNgDLI1JP5z/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 70 amy_1
echo Finished Command 7
echo Finished Command 7 >> %LOGFILE%
echo. >> %LOGFILE%
echo.

REM Command 8
echo Running Command 8...
echo Running Command 8... >> %LOGFILE%
python main_scraper.py "https://www.instagram.com/reel/DJ9gCNgzdux/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ==" 70 amy_2
echo Finished Command 8
echo Finished Command 8 >> %LOGFILE%
echo. >> %LOGFILE%

echo ========================================
echo All commands completed!
echo ========================================
echo ======================================== >> %LOGFILE%
echo All commands completed! >> %LOGFILE%
echo Completed at %date% %time% >> %LOGFILE%
echo ======================================== >> %LOGFILE%
echo Log saved to: %LOGFILE%
pause