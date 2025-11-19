"""
Comment Extractor Module
Handles extraction of comments from Instagram pages and containers.
"""

import time
from selenium.webdriver.common.by import By
from text_validator import (
    is_valid_text, is_valid_username_comment_pair, 
    clean_comment_text, create_comment_key, FOOTER_TERMS
)


def extract_initial_comments(driver, comments_container, processed_comments, raw_output_file=None):
    """
    Extract initial comments before any scrolling
    
    Args:
        driver: WebDriver instance
        comments_container: Comments container element (can be None)
        processed_comments (set): Set to track processed comments
        raw_output_file (str, optional): Path to file for writing raw comments
        
    Returns:
        tuple: (usernames, comments, likes) lists
    """
    if comments_container:
        print("Using comments container for initial extraction")
        # if raw_output_file:
        #     with open(raw_output_file, 'w', encoding='utf-8') as f:
        #         f.write("=== RAW COMMENT EXTRACTION LOG ===\n")
        #         f.write("=== INITIAL EXTRACTION ===\n")
        return extract_comments_from_container(comments_container, processed_comments, raw_output_file)
    else:
        print("No container found, extracting from entire page")
        return extract_comments_fallback(driver, processed_comments)


def extract_comments_from_container(container, processed_comments, raw_output_file=None):
    """
    Extract comments from a specific container
    
    Args:
        container: WebElement container to extract from
        processed_comments (set): Set to track processed comments
        raw_output_file (str, optional): Path to file for writing raw comments
        
    Returns:
        tuple: (usernames, comments, likes) lists
    """
    user_names = []
    user_comments = []
    comment_likes = []
    
    try:
        # Find username links within the container
        username_links = container.find_elements(
            By.XPATH, 
            ".//a[contains(@href, '/') and not(contains(@href, 'explore')) and not(contains(@href, 'accounts'))]"
        )
        print(f"  📋 Found {len(username_links)} potential username links")
        
        # Write raw data to file if provided
        # if raw_output_file:
        #     with open(raw_output_file, 'a', encoding='utf-8') as f:
        #         f.write(f"\n=== SCROLL EXTRACTION - Found {len(username_links)} username links ===\n")
        
        for link in username_links:
            try:
                username = link.text.strip()
                
                # Skip invalid usernames
                if not is_valid_text(username) or username in FOOTER_TERMS:
                    continue
                
                # Find the parent comment container
                parent = _find_comment_parent(link)
                if not parent:
                    continue
                
                # Extract comment text from parent
                comment_text = _extract_comment_text_from_parent(parent, username)
                
                # Write raw data to file (before any filtering)
                # if raw_output_file and comment_text:
                #     with open(raw_output_file, 'a', encoding='utf-8') as f:
                #         f.write(f"RAW: {username} -> {comment_text}\n")
                
                if comment_text and is_valid_username_comment_pair(username, comment_text):
                    if _add_unique_comment(username, comment_text, processed_comments, 
                                         user_names, user_comments, comment_likes):
                        print(f"  {username}: {comment_text[:60]}...")
                        # if raw_output_file:
                        #     with open(raw_output_file, 'a', encoding='utf-8') as f:
                        #         f.write(f"ACCEPTED: {username} -> {comment_text}\n")
            
            except Exception:
                continue
    
    except Exception as e:
        print(f"  Error extracting from container: {e}")
    
    return user_names, user_comments, comment_likes


def extract_comments_fallback(driver, processed_comments):
    """
    Fallback extraction method for when no container is found
    
    Args:
        driver: WebDriver instance
        processed_comments (set): Set to track processed comments
        
    Returns:
        tuple: (usernames, comments, likes) lists
    """
    user_names = []
    user_comments = []
    comment_likes = []
    
    try:
        # Get all spans with dir='auto' from the entire page
        all_spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
        print(f"  📋 Found {len(all_spans)} total spans with dir='auto'")
        
        # Extract meaningful texts
        meaningful_texts = [
            span.text.strip() for span in all_spans 
            if is_valid_text(span.text.strip())
        ]
        
        print(f"  📝 Extracted {len(meaningful_texts)} meaningful text elements")
        
        # Try to pair consecutive texts as username:comment
        i = 0
        while i < len(meaningful_texts) - 1:
            potential_username = meaningful_texts[i]
            potential_comment = meaningful_texts[i + 1]
            
            if is_valid_username_comment_pair(potential_username, potential_comment):
                if _add_unique_comment(potential_username, potential_comment, processed_comments,
                                     user_names, user_comments, comment_likes):
                    print(f" {potential_username}: {potential_comment[:60]}...")
                    i += 2  # Skip both texts
                    continue
            
            i += 1
    
    except Exception as e:
        print(f"  Fallback extraction failed: {e}")
    
    return user_names, user_comments, comment_likes


def scroll_and_extract_comments(driver, comments_container, num_scrolls, processed_comments, raw_output_file=None):
    """
    Scroll the container and extract comments after each scroll
    
    Args:
        driver: WebDriver instance
        comments_container: Comments container element (can be None)
        num_scrolls (int): Number of scroll iterations
        processed_comments (set): Set to track processed comments
        raw_output_file (str, optional): Path to file for writing raw comments
        
    Returns:
        tuple: (usernames, comments, likes) lists
    """
    all_names = []
    all_comments = []
    all_likes = []
    
    if not comments_container:
        print(" No scrollable container found, using page scrolling fallback")
        for i in range(num_scrolls):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            print(f"Page scroll {i+1}/{num_scrolls}")
        return all_names, all_comments, all_likes
    
    print(f"🔄 Scrolling and extracting {num_scrolls} batches...")
    
    for i in range(num_scrolls):
        print(f"\n--- Scroll {i+1}/{num_scrolls} ---")
        
        # Get current state
        initial_height = driver.execute_script("return arguments[0].scrollHeight;", comments_container)
        initial_count = len(all_names)
        
        # Scroll to bottom
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", comments_container)
        print(f"  📜 Scrolled to bottom (height: {initial_height}px)")
        
        # Wait for new content
        time.sleep(4)
        
        # Check if new content loaded
        new_height = driver.execute_script("return arguments[0].scrollHeight;", comments_container)
        print(f" New height: {new_height}px")
        
        if new_height == initial_height:
            print("   No new content loaded, stopping early")
            break
        
        # Extract new comments
        print("  🔍 Extracting new comments...")
        # if raw_output_file:
        #     with open(raw_output_file, 'a', encoding='utf-8') as f:
        #         f.write(f"\n=== SCROLL {i+1} - Height: {initial_height}px -> {new_height}px ===\n")
        new_names, new_comments, new_likes = extract_comments_from_container(comments_container, processed_comments, raw_output_file)
        
        # Add to collections
        all_names.extend(new_names)
        all_comments.extend(new_comments)
        all_likes.extend(new_likes)
        
        new_count = len(all_names) - initial_count
        print(f" Extracted {new_count} new comments (Total: {len(all_names)})")
        
        # Check if reached bottom
        if _is_at_bottom(driver, comments_container):
            print("  🏁 Reached bottom of comments container")
            break
    
    return all_names, all_comments, all_likes


def _find_comment_parent(link):
    """
    Find the parent container that holds the comment text
    
    Args:
        link: WebElement link containing username
        
    Returns:
        WebElement or None: Parent container if found, None otherwise
    """
    try:
        parent = link.find_element(By.XPATH, "./ancestor::*[contains(@class, 'html-div')][1]")
        for _ in range(3):  # Go up a few levels if needed
            try:
                parent = parent.find_element(By.XPATH, "./..")
                if parent.find_elements(By.CSS_SELECTOR, "span[dir='auto']"):
                    break
            except:
                break
        return parent
    except:
        return None


def _extract_comment_text_from_parent(parent, username):
    """
    Extract comment text from parent container
    
    Args:
        parent: WebElement parent container
        username (str): Username to exclude from comment text
        
    Returns:
        str: Comment text if found, empty string otherwise
    """
    try:
        all_spans = parent.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
        comment_text = ""
        
        for span in all_spans:
            text = span.text.strip()
            if (text and text != username and 
                is_valid_text(text, min_length=2) and
                len(text) > len(comment_text)):
                comment_text = text
        
        return comment_text
    except:
        return ""


def _add_unique_comment(username, comment, processed_comments, user_names, user_comments, comment_likes):
    """
    Add comment if it's unique (not already processed)
    
    Args:
        username (str): Username
        comment (str): Comment text
        processed_comments (set): Set of processed comment keys
        user_names (list): List to add username to
        user_comments (list): List to add comment to
        comment_likes (list): List to add likes to
        
    Returns:
        bool: True if comment was added, False if duplicate
    """
    comment_key = create_comment_key(username, comment)
    if comment_key not in processed_comments:
        user_names.append(username)
        user_comments.append(clean_comment_text(comment))
        comment_likes.append(0)
        processed_comments.add(comment_key)
        return True
    return False



def _is_at_bottom(driver, container):
    """
    Check if scrolled to bottom of container
    
    Args:
        driver: WebDriver instance
        container: Container element to check
        
    Returns:
        bool: True if at bottom, False otherwise
    """
    scroll_top = driver.execute_script("return arguments[0].scrollTop;", container)
    client_height = driver.execute_script("return arguments[0].clientHeight;", container)
    scroll_height = driver.execute_script("return arguments[0].scrollHeight;", container)
    return scroll_top + client_height >= scroll_height - 10