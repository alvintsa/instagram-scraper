"""
Script to scrape comments for all posts of a given Instagram username.
Usage:
    python scrape_comments_for_user.py <instagram_username>
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "InstagramPrivSniffer"))
from InstagramPrivSniffer.main import main as sniffer_main
from InstagramPrivSniffer.utils.parser import getArguments
import subprocess

DEFAULT_SCROLLS = 70
MAIN_SCRAPER_PATH = "main_scraper.py"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_comments_for_user.py <instagram_username>")
        sys.exit(1)
    username = sys.argv[1]

    # Step 1: Get post links for the user
    class Args:
        def __init__(self, name=None, dload=None):
            self.name = name
            self.dload = dload
    args = Args(name=username)
    post_links = sniffer_main(args)
    print(f"Found {len(post_links)} posts for user '{username}'")

    # Step 2: Run main_scraper.py for each post link
    for idx, post_link in enumerate(post_links):
        print(f"Scraping comments for post {idx+1}/{len(post_links)}: {post_link}")
        # Output filename: <username>_<idx+1>.csv
        output_filename = f"{username}_{idx+1}.csv"
        cmd = [sys.executable, MAIN_SCRAPER_PATH, post_link, str(DEFAULT_SCROLLS), output_filename]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
