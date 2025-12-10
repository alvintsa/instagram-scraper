#!/bin/bash
# Instagram Auto Scraper - Username Input Version
# This script asks for a username, uses InstagramPrivSniffer to get posts, then scrapes them

# Function to extract Instagram URLs and run scraper
process_posts() {
    local username="$1"
    local temp_file="$2"
    local counter=1
    
    echo ""
    echo "Step 2: Processing found posts..."
    echo "Step 2: Processing found posts..." >> "$LOGFILE"
    
    # Extract Instagram URLs from the temp file - VIDEOS ONLY
    while IFS= read -r line; do
        if [[ $line == *"[VIDEO]"* ]]; then
            # Extract URL (second field after the type)
            url=$(echo "$line" | awk '{print $2}')
            
            if [[ $url == https://www.instagram.com/*/reel/* ]] || [[ $url == https://www.instagram.com/*/tv/* ]]; then
                echo ""
                echo "Running scraper $counter for: $url"
                echo "Running scraper $counter for: $url" >> "$LOGFILE"
                
                # Run the scraper with 30 scrolls and auto-generated filename
                python3 main_scraper.py "$url" 30 "${username}_${counter}"
                
                if [ $? -eq 0 ]; then
                    echo "Successfully completed scraper $counter"
                    echo "Successfully completed scraper $counter" >> "$LOGFILE"
                else
                    echo "Warning: Scraper $counter failed for $url"
                    echo "Warning: Scraper $counter failed for $url" >> "$LOGFILE"
                fi
                
                echo "" >> "$LOGFILE"
                ((counter++))
            fi
        fi
    done < "$temp_file"
}

# Main script starts here
echo "========================================"
echo "Instagram Auto Scraper - Username Mode"
echo "========================================"
echo ""

# Get username from user
read -p "Enter Instagram username (without @): " USERNAME

if [ -z "$USERNAME" ]; then
    echo "Error: No username provided."
    exit 1
fi

echo ""
echo "Target username: $USERNAME"
echo ""

# Set up logging
LOGFILE="auto_scrape_${USERNAME}_log.txt"
echo "" > "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "Instagram Auto Scraper - Username: $USERNAME" | tee -a "$LOGFILE"
echo "Started at $(date)" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "" | tee -a "$LOGFILE"

# Step 1: Use InstagramPrivSniffer to get post links
echo "Step 1: Fetching post links for $USERNAME..." | tee -a "$LOGFILE"

# Change to InstagramPrivSniffer directory
cd "$HOME/Desktop/InstagramPrivSniffer" 2>/dev/null || cd "/Users/$(whoami)/Desktop/InstagramPrivSniffer" 2>/dev/null || {
    echo "Error: Could not find InstagramPrivSniffer directory"
    echo "Please ensure InstagramPrivSniffer is in ~/Desktop/InstagramPrivSniffer"
    exit 1
}

# Run the sniffer and save output
TEMP_POSTS="temp_posts_${USERNAME}.txt"
python3 main.py --name "$USERNAME" > "$TEMP_POSTS" 2>&1

if [ $? -ne 0 ]; then
    echo "Error: Failed to fetch posts from InstagramPrivSniffer" | tee -a "$LOGFILE"
    exit 1
fi

# Step 2: Change to scraper directory and process posts
cd "$HOME/Desktop/ig_Scraper" 2>/dev/null || cd "/Users/$(whoami)/Desktop/ig_Scraper" 2>/dev/null || {
    echo "Error: Could not find ig_Scraper directory"
    echo "Please ensure ig_Scraper is in ~/Desktop/ig_Scraper"
    exit 1
}

# Process the found posts
SNIFFER_TEMP="$HOME/Desktop/InstagramPrivSniffer/$TEMP_POSTS"
if [ ! -f "$SNIFFER_TEMP" ]; then
    SNIFFER_TEMP="/Users/$(whoami)/Desktop/InstagramPrivSniffer/$TEMP_POSTS"
fi

if [ -f "$SNIFFER_TEMP" ]; then
    process_posts "$USERNAME" "$SNIFFER_TEMP"
    
    # Clean up temp file
    rm "$SNIFFER_TEMP" 2>/dev/null
else
    echo "Error: Could not find temp posts file" | tee -a "$LOGFILE"
    exit 1
fi

echo ""
echo "========================================" | tee -a "$LOGFILE"
echo "All posts processed for $USERNAME!" | tee -a "$LOGFILE"
echo "Completed at $(date)" | tee -a "$LOGFILE"
echo "========================================" | tee -a "$LOGFILE"
echo "========================================"
echo "All posts processed for $USERNAME!"
echo "========================================"
echo "Log saved to: $LOGFILE"
echo "Press Enter to exit..."
read