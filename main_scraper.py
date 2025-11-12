"""
Instagram Comment Scraper - Main Driver
Sets up Selenium WebDriver and orchestrates the scraping process.
"""

import sys
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from browser_setup import setup_browser, close_browser
from comment_extractor import extract_initial_comments, scroll_and_extract_comments
from data_processor import export_to_csv, print_results_summary, save_debug_info
from login_handler import login_to_instagram
from page_navigator import navigate_to_post, find_comments_container


def validate_arguments():
    """Validate command line arguments"""
    if len(sys.argv) != 3:
        print("Usage: python main_scraper.py <instagram_post_url> <number_of_scrolls>")
        print("Example: python main_scraper.py https://www.instagram.com/reel/ABC123/ 5")
        sys.exit(1)
    
    try:
        num_scrolls = int(sys.argv[2])
        if num_scrolls < 0:
            raise ValueError("Number of scrolls must be non-negative")
        return sys.argv[1], num_scrolls
    except ValueError as e:
        print(f"Invalid number of scrolls: {e}")
        sys.exit(1)


def main():
    """Main execution function"""
    # Load environment variables
    load_dotenv()
    
    # Validate arguments
    post_url, num_scrolls = validate_arguments()
    
    # Setup browser
    driver, wait = setup_browser(headless=False)
    
    try:
        print(f"\n{'='*60}")
        print("INSTAGRAM COMMENT SCRAPER")
        print(f"{'='*60}")
        
        # Step 1: Login to Instagram
        if not login_to_instagram(driver):
            print("Login failed. Cannot proceed with scraping.")
            return
        
        # Step 2: Navigate to post
        if not navigate_to_post(driver, post_url):
            print("Failed to navigate to post.")
            return
        
        # Initialize results
        all_usernames = []
        all_comments = []
        all_likes = []
        processed_comments = set()
        
        print(f"\n{'='*60}")
        print("STEP-BY-STEP COMMENT EXTRACTION")
        print(f"{'='*60}")
        
        # Step 3: Find comments container
        comments_container = find_comments_container(driver)
        
        # Step 4: Extract initial comments BEFORE scrolling
        print("\nSTEP 1: Extracting initial comments...")
        time.sleep(3)  # Let content settle
        
        # Create raw output file for debugging
        # from datetime import datetime
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # raw_output_file = f"raw_comments_{timestamp}.txt"
        # print(f"Raw extraction data will be saved to: {raw_output_file}")
        raw_output_file = None
        
        initial_names, initial_comments, initial_likes = extract_initial_comments(
            driver, comments_container, processed_comments, raw_output_file
        )
        
        all_usernames.extend(initial_names)
        all_comments.extend(initial_comments)
        all_likes.extend(initial_likes)
        
        print(f"Initial extraction: {len(initial_names)} comments")
        
        # Step 5: Scroll and extract more comments if requested
        if num_scrolls > 0:
            scroll_names, scroll_comments, scroll_likes = scroll_and_extract_comments(
                driver, comments_container, num_scrolls, processed_comments, raw_output_file
            )
            all_usernames.extend(scroll_names)
            all_comments.extend(scroll_comments)
            all_likes.extend(scroll_likes)
        
        # Step 6: Print results and export
        print_results_summary(all_usernames, all_comments)
        export_to_csv(all_usernames, all_comments, all_likes)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        print("\nFull error details:")
        print(traceback.format_exc())
        save_debug_info(driver, error=e)
        
    finally:
        # Always clean up
        close_browser(driver)


if __name__ == "__main__":
    main()