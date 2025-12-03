"""
Data Processor Module
Handles data export, display, and debugging functionality.
"""

import csv
import time
from datetime import datetime


def export_to_csv(usernames, comments, likes, custom_filename=None, post_metadata=None):
    """
    Export comments to CSV file
    
    Args:
        usernames (list): List of usernames
        comments (list): List of comments
        likes (list): List of like counts
        custom_filename (str, optional): Custom filename to use
        post_metadata (dict, optional): Post metadata including caption and date
        
    Returns:
        str or None: Filename if successful, None if failed
    """
    if not usernames or not comments:
        print("\n❌ No comments to export")
        return None
    
    # Use custom filename or create one with timestamp
    if custom_filename:
        csv_filename = custom_filename if custom_filename.endswith('.csv') else f"{custom_filename}.csv"
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"instagram_comments_{timestamp}.csv"
    
    try:
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write metadata section if available
            if post_metadata:
                writer.writerow(['=== POST METADATA ==='])
                writer.writerow(['Post URL', post_metadata.get('post_url', '')])
                writer.writerow(['Post Type', post_metadata.get('post_type', '')])
                writer.writerow(['Post Caption', post_metadata.get('caption', '')])
                writer.writerow(['Post Date', post_metadata.get('date', '')])
                writer.writerow(['Extracted At', post_metadata.get('extraction_time', '')])
                writer.writerow([])  # Empty row separator
            
            # Write comments header and data
            writer.writerow(['=== COMMENTS ==='])
            writer.writerow(['Username', 'Comment', 'Likes'])
            
            for i in range(len(usernames)):
                writer.writerow([usernames[i], comments[i], likes[i]])
        
        print(f"\nComments exported to {csv_filename} successfully!")
        print(f"   Total comments saved: {len(usernames)}")
        if post_metadata:
            print(f"   Post metadata included: {'✅ Caption' if post_metadata.get('caption') else '❌ Caption'}, {'✅ Date' if post_metadata.get('date') else '❌ Date'}")
        return csv_filename
    
    except Exception as e:
        print(f"\nError exporting to CSV: {e}")
        return None


def print_results_summary(usernames, comments):
    """
    Print a summary of extracted comments
    
    Args:
        usernames (list): List of usernames
        comments (list): List of comments
    """
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: Extracted {len(usernames)} comments")
    print(f"{'='*60}")
    
    if usernames:
        print("\nSample comments:")
        for i in range(min(10, len(usernames))):
            comment_preview = comments[i][:80] + ('...' if len(comments[i]) > 80 else '')
            print(f"  {i+1}. {usernames[i]}: {comment_preview}")
    else:
        print("\nNo comments extracted!")


def save_debug_info(driver, error=None):
    """
    Save screenshot and page source for debugging
    
    Args:
        driver: WebDriver instance
        error: Exception object (optional)
    """
    timestamp = int(time.time())
    
    try:
        screenshot_name = f"error_screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\nScreenshot saved as: {screenshot_name}")
    except:
        print("\nCould not save screenshot")
    
    try:
        page_source_name = f"error_page_source_{timestamp}.html"
        with open(page_source_name, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"Page source saved as: {page_source_name}")
    except:
        print("Could not save page source")


def print_extraction_progress(step, message, count=None):
    """
    Print formatted progress messages
    
    Args:
        step (str): Current step identifier
        message (str): Progress message
        count (int, optional): Count to display
    """
    if count is not None:
        print(f"{step} {message}: {count}")
    else:
        print(f"{step} {message}")


def validate_extraction_results(usernames, comments, likes, min_expected=5):
    """
    Validate extraction results and provide feedback
    
    Args:
        usernames (list): List of usernames
        comments (list): List of comments  
        likes (list): List of like counts
        min_expected (int): Minimum expected comments
        
    Returns:
        bool: True if results are satisfactory, False otherwise
    """
    total_comments = len(usernames)
    
    if total_comments == 0:
        print("\nNo comments were extracted. This could indicate:")
        print("   • The post has no comments")
        print("   • Instagram changed their HTML structure")
        print("   • Login was unsuccessful")
        print("   • The post is private or restricted")
        return False
    
    if total_comments < min_expected:
        print(f"\nOnly {total_comments} comments extracted (expected at least {min_expected})")
        print("   Consider increasing scroll count or checking extraction logic")
    
    # Check data consistency
    if len(usernames) != len(comments) or len(comments) != len(likes):
        print("\nData inconsistency detected: mismatched list lengths")
        return False
    
    print(f"\nExtraction successful: {total_comments} comments extracted")
    return True