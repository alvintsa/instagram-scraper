"""
Post Metadata Extractor Module
Handles extraction of post caption, date, and other metadata from Instagram pages.
"""

import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def extract_post_caption(driver):
    """
    Extract the post caption/description
    
    Args:
        driver: WebDriver instance
        
    Returns:
        str: Post caption if found, empty string otherwise
    """
    print("🔍 Extracting post caption...")
    
    caption_selectors = [
        # Main caption in post view
        "article h1",
        "article div[data-testid='post-caption'] span",
        # Caption in span with dir='auto' (common pattern)
        "article span[dir='auto']",
        # Alternative selectors for different Instagram layouts
        "div[role='button'] span[dir='auto']",
        "h1 span",
        # Broader search for caption content
        "span[style*='line-height'] span[dir='auto']",
        # Meta description fallback
        "meta[property='og:description']",
    ]
    
    for selector in caption_selectors:
        try:
            if selector.startswith("meta"):
                # Handle meta tag differently
                element = driver.find_element(By.CSS_SELECTOR, selector)
                caption = element.get_attribute("content")
            else:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                # Find the longest meaningful text (likely the caption)
                caption = ""
                for element in elements:
                    text = element.text.strip()
                    if len(text) > len(caption) and len(text) > 20:  # Longer texts are more likely captions
                        caption = text
            
            if caption and len(caption) > 10:
                print(f"✅ Found caption using selector: {selector}")
                print(f"   Caption preview: {caption[:100]}...")
                return caption.strip()
                
        except Exception as e:
            continue
    
    print("❌ Could not find post caption")
    return ""


def extract_post_date(driver):
    """
    Extract the post date/timestamp
    
    Args:
        driver: WebDriver instance
        
    Returns:
        str: Post date if found, empty string otherwise
    """
    print("🔍 Extracting post date...")
    
    date_selectors = [
        # Time element with datetime attribute
        "time[datetime]",
        "time",
        # Date in span or div
        "span[title*='at ']",
        "div[title*='at ']",
        # Alternative patterns
        "a time",
        "article time",
        # Meta tags for date
        "meta[property='article:published_time']",
        "meta[property='og:updated_time']",
    ]
    
    for selector in date_selectors:
        try:
            if selector.startswith("meta"):
                # Handle meta tag
                element = driver.find_element(By.CSS_SELECTOR, selector)
                date_str = element.get_attribute("content")
                if date_str:
                    print(f"✅ Found date in meta tag: {date_str}")
                    return date_str
            else:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    # Try datetime attribute first
                    datetime_attr = element.get_attribute("datetime")
                    if datetime_attr:
                        print(f"✅ Found date using datetime attribute: {datetime_attr}")
                        return datetime_attr
                    
                    # Try title attribute
                    title_attr = element.get_attribute("title")
                    if title_attr and ("at " in title_attr.lower() or "ago" in title_attr.lower()):
                        print(f"✅ Found date in title: {title_attr}")
                        return title_attr
                    
                    # Try text content
                    text = element.text.strip()
                    if text and ("ago" in text.lower() or "at " in text.lower() or len(text) > 5):
                        print(f"✅ Found date text: {text}")
                        return text
                        
        except Exception as e:
            continue
    
    print("❌ Could not find post date")
    return ""


def extract_post_metadata(driver, post_url):
    """
    Extract comprehensive post metadata
    
    Args:
        driver: WebDriver instance
        post_url: URL of the post
        
    Returns:
        dict: Dictionary containing post metadata
    """
    print(f"\n{'='*50}")
    print("EXTRACTING POST METADATA")
    print(f"{'='*50}")
    
    # Wait a moment for page to fully load
    time.sleep(2)
    
    metadata = {
        "post_url": post_url,
        "caption": "",
        "date": "",
        "extraction_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Extract caption
    metadata["caption"] = extract_post_caption(driver)
    
    # Extract date
    metadata["date"] = extract_post_date(driver)
    
    # Additional metadata we could extract
    try:
        # Try to get post type (photo, video, reel, etc.)
        if "/reel/" in post_url:
            metadata["post_type"] = "reel"
        elif "/p/" in post_url:
            metadata["post_type"] = "post"
        else:
            metadata["post_type"] = "unknown"
    except:
        metadata["post_type"] = "unknown"
    
    print(f"\n📋 Post Metadata Summary:")
    print(f"   Type: {metadata['post_type']}")
    print(f"   Caption: {'✅ Found' if metadata['caption'] else '❌ Not found'}")
    print(f"   Date: {'✅ Found' if metadata['date'] else '❌ Not found'}")
    print(f"   Extracted at: {metadata['extraction_time']}")
    
    return metadata


def format_caption_for_csv(caption):
    """
    Format caption for CSV export (handle newlines, quotes, etc.)
    
    Args:
        caption (str): Raw caption text
        
    Returns:
        str: Formatted caption suitable for CSV
    """
    if not caption:
        return ""
    
    # Replace newlines with spaces
    formatted = caption.replace('\n', ' ').replace('\r', ' ')
    
    # Remove excessive whitespace
    formatted = ' '.join(formatted.split())
    
    # Truncate if too long (optional)
    if len(formatted) > 1000:
        formatted = formatted[:997] + "..."
    
    return formatted


def format_date_for_csv(date_str):
    """
    Format date for CSV export
    
    Args:
        date_str (str): Raw date string
        
    Returns:
        str: Formatted date suitable for CSV
    """
    if not date_str:
        return ""
    
    # Clean up common date formats
    formatted = date_str.strip()
    
    # Remove extra whitespace
    formatted = ' '.join(formatted.split())
    
    return formatted