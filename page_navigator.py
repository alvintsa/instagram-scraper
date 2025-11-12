"""
Page Navigator Module
Handles navigation and page element discovery.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def navigate_to_post(driver, post_url):
    """
    Navigate to the Instagram post and wait for it to load
    
    Args:
        driver: WebDriver instance
        post_url (str): URL of the Instagram post
        
    Returns:
        bool: True if navigation successful, False otherwise
    """
    print(f"Navigating to post: {post_url}")
    driver.get(post_url)
    time.sleep(5)
    
    # Check if we successfully navigated (basic check)
    current_url = driver.current_url
    if "instagram.com" not in current_url:
        print("Failed to navigate to Instagram")
        return False
    
    # Try to find article element but don't fail if not found
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "article"))
        )
        print("Article loaded successfully")
    except:
        print("Warning: Could not find article element, but proceeding anyway")
    
    print("✅ Navigation completed successfully")
    return True


def find_comments_container(driver):
    """
    Find the scrollable comments container
    
    Args:
        driver: WebDriver instance
        
    Returns:
        WebElement or None: Comments container element if found, None otherwise
    """
    print("Looking for comments container...")
    
    # Primary selector
    try:
        container = driver.find_element(By.CSS_SELECTOR, "div.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6")
        print("Found scrollable comments container!")
        return container
    except:
        pass
    
    # Fallback selectors
    fallback_selectors = [
        "div[class*='x5yr21d'][class*='xw2csxc']",
        "div[class*='x5yr21d']",
        "div[style*='overflow']",
    ]
    
    for selector in fallback_selectors:
        try:
            container = driver.find_element(By.CSS_SELECTOR, selector)
            print(f"Found comments container with fallback: {selector}")
            return container
        except:
            continue
    
    print("No comments container found")
    return None