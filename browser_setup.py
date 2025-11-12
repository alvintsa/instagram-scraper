"""
Browser Setup Module
Handles WebDriver initialization and cleanup.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def setup_browser(headless=False):
    """
    Setup Firefox browser with options
    
    Args:
        headless (bool): Whether to run in headless mode
        
    Returns:
        tuple: (driver, wait) - WebDriver instance and WebDriverWait instance
    """
    options = webdriver.FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    if headless:
        options.add_argument('--headless')
    
    service = webdriver.FirefoxService()
    driver = webdriver.Firefox(service=service, options=options)
    wait = WebDriverWait(driver, 10)
    
    print("Browser initialized successfully")
    return driver, wait


def close_browser(driver):
    """
    Clean up and close the browser
    
    Args:
        driver: WebDriver instance to close
    """
    try:
        if driver:
            driver.quit()
            print("\nBrowser closed successfully")
    except Exception as e:
        print(f"\nError closing browser: {e}")