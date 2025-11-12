from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys
import os
import re
from dotenv import load_dotenv
from prototypes.login import perform_instagram_login

# Load environment variables from .env file
load_dotenv()

# Check for required arguments
if len(sys.argv) != 3:
    print("Usage: python scraper.py <instagram_post_url> <number_of_load_more_clicks>")
    sys.exit(1)

# Setup Firefox driver
options = webdriver.FirefoxOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# Uncomment next line for headless mode
# options.add_argument('--headless')

service = webdriver.FirefoxService()
driver = webdriver.Firefox(service=service, options=options)
wait = WebDriverWait(driver, 10)

def extract_comments_fallback(driver, processed_comments):
    """Fallback extraction method for when no container is found"""
    user_names = []
    user_comments = []
    comment_likes = []
    
    # Common footer/navigation terms to filter out
    footer_terms = {"Meta", "Help", "Locations", "About", "Press", "API", "Jobs", "Privacy", 
                    "Terms", "Contact", "Language", "Meta Verified", "Threads", "Follow", 
                    "Following", "Like", "Reply", "View replies", "View all replies",
                    "Log in", "Sign up", "More", "Liked", "Add a comment", "Post"}
    
    try:
        # Get all spans with dir='auto' from the entire page
        all_spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
        print(f"  Found {len(all_spans)} total spans with dir='auto'")
        
        # Extract all meaningful text
        meaningful_texts = []
        for span in all_spans:
            text = span.text.strip()
            if (text and len(text) > 2 and text not in footer_terms and
                not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago|like|likes)$', text, re.IGNORECASE)):
                meaningful_texts.append(text)
        
        print(f"  Extracted {len(meaningful_texts)} meaningful text elements")
        
        # Try to pair consecutive texts as username:comment
        i = 0
        while i < len(meaningful_texts) - 1:
            potential_username = meaningful_texts[i]
            potential_comment = meaningful_texts[i + 1]
            
            # Check if this looks like a username-comment pair
            if (len(potential_username) < 30 and 
                len(potential_comment) > len(potential_username) and
                len(potential_comment) > 15 and  # Longer minimum for meaningful comments
                potential_username != potential_comment and
                not potential_username.endswith('Follow') and
                not potential_comment.startswith('Follow') and
                not re.match(r'^(Reply|View|Follow|Following|Like|Unlike)$', potential_username, re.IGNORECASE) and
                not re.match(r'^(Reply|View|Follow|Following|Like|Unlike)$', potential_comment, re.IGNORECASE)):
                
                comment_key = f"{potential_username}:{potential_comment[:50]}"
                if comment_key not in processed_comments:
                    user_names.append(potential_username)
                    user_comments.append(potential_comment.replace('\n', ' ').strip())
                    comment_likes.append(0)
                    processed_comments.add(comment_key)
                    print(f"    ✓ {potential_username}: {potential_comment[:60]}...")
                    i += 2  # Skip both texts
                    continue
            
            i += 1
                    
    except Exception as e:
        print(f"  Fallback extraction failed: {e}")
    
    return user_names, user_comments, comment_likes

def extract_comments_from_container(container, processed_comments):
    """Extract comments from a given container, avoiding duplicates"""
    user_names = []
    user_comments = []
    comment_likes = []
    
    # Common footer/navigation terms to filter out
    footer_terms = {"Meta", "Help", "Locations", "About", "Press", "API", "Jobs", "Privacy", 
                    "Terms", "Contact", "Language", "Meta Verified", "Threads", "Follow", 
                    "Following", "Like", "Reply", "View replies", "View all replies",
                    "Log in", "Sign up", "More", "Liked", "Add a comment", "Post"}
    
    try:
        # Look for username links within the container
        username_links = container.find_elements(By.XPATH, ".//a[contains(@href, '/') and not(contains(@href, 'explore')) and not(contains(@href, 'accounts'))]")
        print(f"  Found {len(username_links)} potential username links")
        
        for link in username_links:
            try:
                username = link.text.strip()
                
                # Skip invalid usernames
                if (not username or username in footer_terms or 
                    len(username) > 30 or len(username) < 2 or 
                    username.startswith('@') or username.endswith('Follow')):
                    continue
                
                # Find the parent comment container
                try:
                    # Look for the nearest parent that contains comment text
                    parent = link.find_element(By.XPATH, "./ancestor::*[contains(@class, 'html-div')][1]")
                    for _ in range(3):  # Go up a few levels if needed
                        try:
                            parent = parent.find_element(By.XPATH, "./..")
                            if parent.find_elements(By.CSS_SELECTOR, "span[dir='auto']"):
                                break
                        except:
                            break
                except:
                    continue
                
                # Get all text spans in this container
                all_spans = parent.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
                
                # Find comment text (longest meaningful text that's not the username)
                comment_text = ""
                for span in all_spans:
                    text = span.text.strip()
                    if (text and text != username and 
                        text not in footer_terms and
                        len(text) > len(comment_text) and
                        len(text) > 10 and  # Longer minimum for meaningful comments
                        not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago|like|likes)$', text, re.IGNORECASE) and
                        not re.match(r'^(Reply|View|Follow|Following)$', text, re.IGNORECASE)):
                        comment_text = text
                
                if comment_text and len(comment_text) > 10:
                    comment_key = f"{username}:{comment_text[:50]}"  # Use truncated key to avoid exact duplicates
                    if comment_key not in processed_comments:
                        user_names.append(username)
                        user_comments.append(comment_text.replace('\n', ' ').strip())
                        comment_likes.append(0)
                        processed_comments.add(comment_key)
                        print(f"    ✓ {username}: {comment_text[:60]}...")
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"  Error extracting from container: {e}")
    
    return user_names, user_comments, comment_likes

try:
    # Perform Instagram login using the login module
    login_success = perform_instagram_login(driver, max_attempts=3)
    
    if not login_success:
        print("❌ Login failed. Cannot proceed with scraping.")
        sys.exit(1)
    
    print("✅ Login completed successfully!")

    # Navigate to the post
    print(f"Navigating to post: {sys.argv[1]}")
    driver.get(sys.argv[1])
    time.sleep(5)
    
    # Wait for article to load
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        print("Article loaded successfully")
    except:
        print("Warning: Could not find article element")

    # Initialize variables
    num_loads = int(sys.argv[2])
    all_user_names = []
    all_user_comments = []
    all_comment_likes = []
    processed_comments = set()  # To avoid duplicates

    print(f"\n{'='*60}")
    print("STEP-BY-STEP COMMENT EXTRACTION")
    print(f"{'='*60}")

    # Find the scrollable comments container
    comments_container = None
    try:
        comments_container = driver.find_element(By.CSS_SELECTOR, "div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")
        print("✓ Found scrollable comments container!")
    except:
        # Fallback selectors
        selectors_to_try = [
            "div[class*='x5yr21d'][class*='xw2csxc']",
            "div[class*='x5yr21d']",
            "div[style*='overflow']",
        ]
        
        for selector in selectors_to_try:
            try:
                comments_container = driver.find_element(By.CSS_SELECTOR, selector)
                print(f"✓ Found comments container with fallback: {selector}")
                break
            except:
                continue

    # STEP 1: Extract initial comments (first ~15) BEFORE any scrolling
    print("\n🔍 STEP 1: Extracting initial comments...")
    time.sleep(3)  # Let content settle completely
    
    # Always try to extract initial comments from the page, even without container
    if comments_container:
        print("✓ Using comments container for initial extraction")
        initial_names, initial_comments, initial_likes = extract_comments_from_container(comments_container, processed_comments)
    else:
        print("⚠️ No container found, extracting from entire page")
        # Fallback: extract from entire page initially
        initial_names, initial_comments, initial_likes = extract_comments_fallback(driver, processed_comments)
    
    all_user_names.extend(initial_names)
    all_user_comments.extend(initial_comments)
    all_comment_likes.extend(initial_likes)
    
    print(f"✅ Initial extraction: {len(initial_names)} comments")
    
    # Only proceed with scrolling if we have a container and want more comments
    if comments_container and num_loads > 0:
        # STEP 2: Scroll and extract after each scroll
        print(f"\n🔄 STEP 2: Scrolling and extracting {num_loads} batches...")
        
        for i in range(num_loads):
            print(f"\n--- Scroll {i+1}/{num_loads} ---")
            
            # Get current state
            initial_height = driver.execute_script("return arguments[0].scrollHeight;", comments_container)
            initial_count = len(all_user_names)
            
            # Scroll to the bottom of the container
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", comments_container)
            print(f"  📜 Scrolled to bottom (height: {initial_height}px)")
            
            # Wait for new content to load
            time.sleep(4)  # Increased wait time
            
            # Check if new content loaded
            new_height = driver.execute_script("return arguments[0].scrollHeight;", comments_container)
            print(f"  📏 New height: {new_height}px")
            
            if new_height == initial_height:
                print(f"  📍 No new content loaded, stopping early")
                break
            
            # Extract new comments from the container
            print(f"  🔍 Extracting new comments...")
            new_names, new_comments, new_likes = extract_comments_from_container(comments_container, processed_comments)
            
            # Add new comments to our collections
            all_user_names.extend(new_names)
            all_user_comments.extend(new_comments)
            all_comment_likes.extend(new_likes)
            
            new_count = len(all_user_names) - initial_count
            print(f"  ✅ Extracted {new_count} new comments (Total: {len(all_user_names)})")
            
            # Check if we've reached the bottom
            scroll_top = driver.execute_script("return arguments[0].scrollTop;", comments_container)
            client_height = driver.execute_script("return arguments[0].clientHeight;", comments_container)
            scroll_height = driver.execute_script("return arguments[0].scrollHeight;", comments_container)
            
            if scroll_top + client_height >= scroll_height - 10:
                print(f"  📍 Reached bottom of comments container")
                break
    elif not comments_container:
        print("❌ No scrollable container found, using page scrolling fallback")
        for i in range(num_loads):
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            print(f"Page scroll {i+1}/{num_loads}")
    else:
        print("⏭️ No additional scrolling requested (num_loads = 0)")

    # Final extraction using brute force if we didn't get many comments
    if len(all_user_names) < 10:
        print(f"\n🚀 FALLBACK: Brute force extraction (current: {len(all_user_names)} comments)...")
        try:
            # Get all spans with dir='auto' from the entire page
            all_spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
            print(f"  Found {len(all_spans)} total spans with dir='auto'")
            
            # Common footer/navigation terms to filter out
            footer_terms = {"Meta", "Help", "Locations", "About", "Press", "API", "Jobs", "Privacy", 
                            "Terms", "Contact", "Language", "Meta Verified", "Threads", "Follow", 
                            "Following", "Like", "Reply", "View replies", "View all replies",
                            "Log in", "Sign up", "More", "Liked", "Add a comment", "Post"}
            
            # Extract all meaningful text
            meaningful_texts = []
            for span in all_spans:
                text = span.text.strip()
                if (text and len(text) > 2 and text not in footer_terms and
                    not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago|like|likes)$', text, re.IGNORECASE)):
                    meaningful_texts.append(text)
            
            print(f"  Extracted {len(meaningful_texts)} meaningful text elements")
            
            # Try to pair consecutive texts as username:comment
            i = 0
            while i < len(meaningful_texts) - 1:
                potential_username = meaningful_texts[i]
                potential_comment = meaningful_texts[i + 1]
                
                # Check if this looks like a username-comment pair
                if (len(potential_username) < 30 and 
                    len(potential_comment) > len(potential_username) and
                    len(potential_comment) > 15 and  # Longer minimum for meaningful comments
                    potential_username != potential_comment and
                    not potential_username.endswith('Follow') and
                    not potential_comment.startswith('Follow') and
                    not re.match(r'^(Reply|View|Follow|Following|Like|Unlike)$', potential_username, re.IGNORECASE) and
                    not re.match(r'^(Reply|View|Follow|Following|Like|Unlike)$', potential_comment, re.IGNORECASE)):
                    
                    comment_key = f"{potential_username}:{potential_comment[:50]}"
                    if comment_key not in processed_comments:
                        all_user_names.append(potential_username)
                        all_user_comments.append(potential_comment.replace('\n', ' ').strip())
                        all_comment_likes.append(0)
                        processed_comments.add(comment_key)
                        print(f"    ✓ {potential_username}: {potential_comment[:60]}...")
                        i += 2  # Skip both texts
                        continue
                
                i += 1
            
            print(f"  ✅ Fallback extracted {len(all_user_names)} total comments")
                        
        except Exception as e:
            print(f"  ❌ Fallback extraction failed: {e}")

    # Final results
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: Extracted {len(all_user_names)} comments")
    print(f"{'='*60}")

    # Print sample comments for verification
    if all_user_names:
        print("\n📝 Sample comments:")
        for i in range(min(10, len(all_user_names))):
            print(f"  {i+1}. {all_user_names[i]}: {all_user_comments[i][:80]}{'...' if len(all_user_comments[i]) > 80 else ''}")
    else:
        print("\n❌ No comments extracted!")

    # Export to CSV
    if all_user_names and all_user_comments:
        import csv
        from datetime import datetime
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"instagram_comments_{timestamp}.csv"
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Username', 'Comment', 'Likes'])
            # Write data
            for i in range(len(all_user_names)):
                writer.writerow([all_user_names[i], all_user_comments[i], all_comment_likes[i]])
        
        print(f"\n💾 Comments exported to {csv_filename} successfully!")
        print(f"   Total comments saved: {len(all_user_names)}")
    else:
        print("\n❌ No comments to export")

except Exception as e:
    import traceback
    print(f"\n❌ An error occurred: {e}")
    print("\n📋 Full error details:")
    print(traceback.format_exc())
    
    # Save a screenshot for debugging
    try:
        screenshot_name = f"error_screenshot_{int(time.time())}.png"
        driver.save_screenshot(screenshot_name)
        print(f"\n📸 Screenshot saved as: {screenshot_name}")
    except:
        print("\n❌ Could not save screenshot")
    
    # Save page source for debugging
    try:
        page_source_name = f"error_page_source_{int(time.time())}.html"
        with open(page_source_name, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 Page source saved as: {page_source_name}")
    except:
        print("❌ Could not save page source")
        
finally:
    try:
        driver.quit()
        print("\n✓ Browser closed successfully")
    except:
        print("\n❌ Error closing browser")