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

# Load environment variables from .env file
load_dotenv()
# Get credentials from environment variables
IG_USERNAME = os.getenv('IG_USERNAME')
IG_PASSWORD = os.getenv('IG_PASSWORD')

if not IG_USERNAME or not IG_PASSWORD:
    print("Error: Set IG_USERNAME and IG_PASSWORD environment variables")
    print("Usage: IG_USERNAME=your_user IG_PASSWORD=your_pass python scraper.py <post_url> <num_loads>")
    sys.exit(1)

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

try:
    # Navigate to Instagram
    print("Navigating to Instagram...")
    driver.get("https://www.instagram.com/")
    time.sleep(3)

    # Login
    print("Logging in...")
    username_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_input = driver.find_element(By.NAME, "password")
    
    username_input.send_keys(IG_USERNAME)
    password_input.send_keys(IG_PASSWORD)
    password_input.submit()
    
    # Wait for login to complete
    time.sleep(5)
    
    # Handle "Save Login Info" popup if it appears
    try:
        not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now.click()
        time.sleep(2)
    except:
        pass
    
    # Handle "Turn on Notifications" popup if it appears
    try:
        not_now = driver.find_element(By.XPATH, "//button[contains(text(), 'Not Now')]")
        not_now.click()
        time.sleep(2)
    except:
        pass

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
    
    # Scroll down to load comments section
    print("Scrolling to load comments...")
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(1)

    # Try to load more comments
    num_loads = int(sys.argv[2])
    print(f"Attempting to load {num_loads} more comment batches...")
    
    loads_completed = 0
    for i in range(num_loads):
        try:
            # Look for "Load more comments" button with multiple selectors
            load_more_selectors = [
                "//button[contains(text(), 'Load more comments')]",
                "//button[contains(text(), 'View more comments')]",
                "//span[contains(text(), 'Load more comments')]/parent::button",
                "//span[contains(text(), 'View more comments')]/parent::button",
                "[data-testid='load-more-comments']"
            ]
            
            load_more_button = None
            for selector in load_more_selectors:
                try:
                    if selector.startswith("//"):
                        load_more_button = driver.find_element(By.XPATH, selector)
                    else:
                        load_more_button = driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except:
                    continue
            
            if load_more_button and load_more_button.is_displayed():
                driver.execute_script("arguments[0].click();", load_more_button)
                print(f"Loaded batch {i+1}")
                loads_completed += 1
                time.sleep(3)
            else:
                print(f"No more 'Load more comments' button found at attempt {i+1}")
                break
                
        except Exception as e:
            print(f"Error loading more comments at attempt {i+1}: {e}")
            break

    print(f"Completed {loads_completed} comment loads")

    # Extract comments using improved approach
    print("\n" + "="*60)
    print("EXTRACTING COMMENTS")
    print("="*60)
    user_names = []
    user_comments = []
    comment_likes = []
    
    # Wait for comments section to fully load
    time.sleep(2)
    
    # Debug: Check what elements we can find
    print("\nDEBUG: Checking page structure...")
    try:
        articles = driver.find_elements(By.TAG_NAME, "article")
        print(f"  Found {len(articles)} article elements")
        
        uls = driver.find_elements(By.TAG_NAME, "ul")
        print(f"  Found {len(uls)} ul elements")
        
        lis = driver.find_elements(By.TAG_NAME, "li")
        print(f"  Found {len(lis)} li elements")
        
        spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
        print(f"  Found {len(spans)} span[dir='auto'] elements")
        
        # Save page source for debugging
        with open("debug_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("  Saved page source to debug_page_source.html")
    except Exception as e:
        print(f"  Debug check failed: {e}")
    
    processed_comments = set()  # To avoid duplicates
    
    # Common footer/navigation terms to filter out
    footer_terms = {"Meta", "Help", "Locations", "About", "Press", "API", "Jobs", "Privacy", 
                    "Terms", "Contact", "Language", "Meta Verified", "Threads", "Follow", 
                    "Following", "Like", "Reply", "View replies", "View all replies",
                    "Log in", "Sign up", "More", "Liked"}
    
    # Method 1: Look for any clickable username links followed by text
    print("\nMethod 1: Looking for username links...")
    try:
        # Find all links that look like usernames (contain @)
        username_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/') and not(contains(@href, 'explore')) and not(contains(@href, 'accounts'))]")
        print(f"Found {len(username_links)} potential username links")
        
        for link in username_links[:100]:  # Limit to avoid performance issues
            try:
                username = link.text.strip()
                
                # Skip invalid usernames
                if not username or username in footer_terms or len(username) > 30 or len(username) < 2:
                    continue
                
                # Get parent container (go up a few levels to get the comment container)
                try:
                    parent = link.find_element(By.XPATH, "./ancestor::li[1]")
                except:
                    try:
                        parent = link.find_element(By.XPATH, "./ancestor::div[3]")
                    except:
                        continue
                
                # Get all text spans in this container
                all_spans = parent.find_elements(By.CSS_SELECTOR, "span")
                
                # Find comment text (longest text that's not the username)
                comment_text = ""
                for span in all_spans:
                    text = span.text.strip()
                    if (text and text != username and 
                        text not in footer_terms and
                        len(text) > len(comment_text) and
                        len(text) > 3 and
                        not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago)$', text, re.IGNORECASE)):
                        comment_text = text
                
                if comment_text and len(comment_text) > 3:
                    comment_key = f"{username}:{comment_text}"
                    if comment_key not in processed_comments:
                        user_names.append(username)
                        user_comments.append(comment_text.replace('\n', ' ').strip())
                        comment_likes.append(0)
                        processed_comments.add(comment_key)
                        print(f"  ✓ {username}: {comment_text[:60]}...")
            except Exception as e:
                continue
        
        print(f"Method 1 extracted {len(user_names)} comments")
        
    except Exception as e:
        print(f"Method 1 failed: {e}")
    
    # Method 2: Brute force - get ALL spans and try to pair them
    if len(user_names) < 5:
        print("\nMethod 2: Brute force span pairing...")
        try:
            # Get all spans with dir='auto'
            all_spans = driver.find_elements(By.CSS_SELECTOR, "span[dir='auto']")
            print(f"Found {len(all_spans)} total spans with dir='auto'")
            
            # Extract all text
            all_texts = []
            for span in all_spans:
                text = span.text.strip()
                if text and len(text) > 1:
                    all_texts.append(text)
            
            print(f"Extracted {len(all_texts)} non-empty text elements")
            print("Sample texts:", all_texts[:20])
            
            # Try to pair consecutive texts as username:comment
            i = 0
            while i < len(all_texts) - 1:
                potential_username = all_texts[i]
                potential_comment = all_texts[i + 1]
                
                # Check if this looks like a username-comment pair
                if (potential_username not in footer_terms and
                    potential_comment not in footer_terms and
                    len(potential_username) < 30 and 
                    len(potential_comment) > len(potential_username) and
                    len(potential_comment) > 5 and
                    potential_username != potential_comment and
                    not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago)$', potential_username, re.IGNORECASE) and
                    not re.match(r'^\d+\s*(h|m|d|w|s|mo|y|ago)$', potential_comment, re.IGNORECASE)):
                    
                    comment_key = f"{potential_username}:{potential_comment}"
                    if comment_key not in processed_comments:
                        user_names.append(potential_username)
                        user_comments.append(potential_comment.replace('\n', ' ').strip())
                        comment_likes.append(0)
                        processed_comments.add(comment_key)
                        print(f"  ✓ {potential_username}: {potential_comment[:60]}...")
                        i += 2  # Skip both texts
                        continue
                
                i += 1
            
            print(f"Method 2 extracted {len(user_names)} total comments")
                        
        except Exception as e:
            print(f"Method 2 failed: {e}")

    print(f"\n{'='*60}")
    print(f"Extracted {len(user_names)} total comments")
    print(f"{'='*60}")
    
    # Print first few comments for verification
    if user_names:
        print("\nSample comments:")
        for i in range(min(5, len(user_names))):
            print(f"{i+1}. {user_names[i]} ({comment_likes[i]} likes): {user_comments[i][:80]}...")
    
    # Export to CSV
    if user_names and user_comments:
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
            for i in range(len(user_names)):
                writer.writerow([user_names[i], user_comments[i], comment_likes[i]])
        
        print(f"\n✓ Comments exported to {csv_filename} successfully!")
        print(f"  Total comments saved: {len(user_names)}")
    else:
        print("\n✗ No comments to export")

except Exception as e:
    import traceback
    print(f"An error occurred: {e}")
    print(traceback.format_exc())
finally:
    driver.quit()