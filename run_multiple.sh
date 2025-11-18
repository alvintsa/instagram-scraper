#!/bin/bash
# Instagram Scraper - Multiple Commands Runner for Mac/Linux
# Edit the URLs and parameters below to customize your runs

LOGFILE="batch_run_log.txt"
echo "" > "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "Instagram Comment Scraper - Batch Runner" | tee -a "$LOGFILE"
echo "Started at $(date)" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

echo "========================================"
echo "Instagram Comment Scraper - Batch Runner"
echo "========================================"
echo ""

# Command 1
echo "Running Command 1..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DQYuvtCEtT1/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 masterwen_hao_1
echo "Finished Command 1" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 2
echo "Running Command 2..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/CZze5EshBlQ/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 doobydobap_1
echo "Finished Command 2" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 3
echo "Running Command 3..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DLIAIhwMcul/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 max_not_beer_1
echo "Finished Command 3" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 4
echo "Running Command 4..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/C2e_PijS8EU/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 50 max_not_beer_2
echo "Finished Command 4" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 5
echo "Running Command 5..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DL85Dw1xzo9/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 dabin_1
echo "Finished Command 5" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 6
echo "Running Command 6..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DHwBtM9svyf/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 khantrast_1
echo "Finished Command 6" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 7
echo "Running Command 7..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DNapbbnNuwi/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 50 austinbchen_1
echo "Finished Command 7" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 8
echo "Running Command 8..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DFQC-N3uvir/?igsh=cnJ6MHYwejlwdjMw 70 austinbchen_2
echo "Finished Command 8" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 9
echo "Running Command 9..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DGMcQsHOObF/?igsh=MWdmZXZmejlqbXRjNA%3D%3D 50 pathradecha_1
echo "Finished Command 9" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 10
echo "Running Command 10..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DKjfhMZzAE3/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 50 xinchen9__1
echo "Finished Command 10" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 11
echo "Running Command 11..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DOB55Bukn7w/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 50 rayjlau_1
echo "Finished Command 11" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Command 12
echo "Running Command 12..." | tee -a "$LOGFILE"
python3 main_scraper.py https://www.instagram.com/reel/DNknatAPc80/?utm_source=ig_web_copy_link&igsh=NTc4MTIwNjQ2YQ== 70 FAKER_1
echo "Finished Command 12" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"




echo "========================================" | tee -a "$LOGFILE"
echo "All commands completed!" | tee -a "$LOGFILE"
echo "Completed at $(date)" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "========================================"
echo "All commands completed!"
echo "========================================"
echo "Log saved to: $LOGFILE"
echo "Press Enter to exit..."
read