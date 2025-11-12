"""
Login Handler Module
Handles Instagram authentication.
"""

from prototypes.login import perform_instagram_login


def login_to_instagram(driver, max_attempts=3):
    """
    Login to Instagram using external login module
    
    Args:
        driver: WebDriver instance
        max_attempts (int): Maximum number of login attempts
        
    Returns:
        bool: True if login successful, False otherwise
    """
    print("Logging into Instagram...")
    login_success = perform_instagram_login(driver, max_attempts=max_attempts)
    
    if not login_success:
        print("Login failed. Cannot proceed with scraping.")
        return False
    
    print("Login completed successfully!")
    return True