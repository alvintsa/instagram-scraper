"""
Instagram Login Module
Handles all Instagram login functionality including cookie consent, login attempts, and popup handling.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import os
from dotenv import load_dotenv


class InstagramLogin:
    """Handles Instagram login process with multiple retry attempts and popup handling"""
    
    def __init__(self, driver, wait_timeout=10):
        """
        Initialize Instagram login handler
        
        Args:
            driver: Selenium WebDriver instance
            wait_timeout: Default wait timeout for elements
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        
        # Load credentials from environment
        load_dotenv()
        self.username = os.getenv('IG_USERNAME')
        self.password = os.getenv('IG_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("Missing Instagram credentials. Set IG_USERNAME and IG_PASSWORD in .env file")
    
    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            accept_cookies = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'Allow') or contains(text(), 'Only allow essential')]"))
            )
            accept_cookies.click()
            print("✓ Accepted cookies")
            time.sleep(2)
            return True
        except:
            print("No cookie popup found")
            return False
    
    def find_username_input(self):
        """Try multiple selectors to find username input field"""
        username_selectors = [
            (By.NAME, "username"),
            (By.CSS_SELECTOR, "input[name='username']"),
            (By.CSS_SELECTOR, "input[aria-label='Phone number, username, or email']"),
            (By.XPATH, "//input[@name='username']"),
            (By.XPATH, "//input[contains(@aria-label, 'username')]")
        ]
        
        for selector_type, selector_value in username_selectors:
            try:
                username_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                print(f"✓ Found username input with selector: {selector_type}, {selector_value}")
                return username_input
            except:
                continue
        
        raise Exception("Could not find username input field")
    
    def find_password_input(self):
        """Try multiple selectors to find password input field"""
        password_selectors = [
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[name='password']"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@name='password']"),
            (By.XPATH, "//input[@type='password']")
        ]
        
        for selector_type, selector_value in password_selectors:
            try:
                password_input = self.driver.find_element(selector_type, selector_value)
                print(f"✓ Found password input with selector: {selector_type}, {selector_value}")
                return password_input
            except:
                continue
        
        raise Exception("Could not find password input field")
    
    def find_and_click_login_button(self, password_input):
        """Try to find and click login button, fallback to submit()"""
        login_selectors = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Log in') or contains(text(), 'Log In')]"),
            (By.XPATH, "//button[@type='submit']"),
            (By.CSS_SELECTOR, "div[role='button'][tabindex='0']")  # Sometimes Instagram uses div as button
        ]
        
        for selector_type, selector_value in login_selectors:
            try:
                login_button = self.driver.find_element(selector_type, selector_value)
                if login_button.is_displayed():
                    print(f"✓ Found login button with selector: {selector_type}, {selector_value}")
                    login_button.click()
                    print("✓ Clicked login button")
                    return True
            except:
                continue
        
        # Fallback to submit()
        password_input.submit()
        print("✓ Used submit() as fallback")
        return True
    
    def attempt_login(self):
        """Attempt to login once with current credentials"""
        try:
            # Find input fields
            username_input = self.find_username_input()
            password_input = self.find_password_input()
            
            # Clear fields and enter credentials
            username_input.clear()
            password_input.clear()
            time.sleep(1)
            
            username_input.send_keys(self.username)
            time.sleep(1)
            password_input.send_keys(self.password)
            time.sleep(1)
            
            # Submit login
            self.find_and_click_login_button(password_input)
            
            # Wait for login to complete
            print("Waiting for login to complete...")
            time.sleep(5)
            
            # Check if login was successful
            current_url = self.driver.current_url
            print(f"Current URL after login: {current_url}")
            
            if "login" not in current_url.lower():
                print("✓ Login appears successful!")
                return True
            else:
                print("Login attempt failed - still on login page")
                return False
                
        except Exception as e:
            print(f"Login attempt error: {e}")
            return False
    
    def handle_post_login_popups(self):
        """Handle various popups that appear after successful login"""
        popup_attempts = 0
        max_popup_attempts = 3
        
        while popup_attempts < max_popup_attempts:
            popup_found = False
            
            # Handle "Save Login Info" popup
            try:
                not_now_selectors = [
                    "//button[contains(text(), 'Not Now') or contains(text(), 'Not now')]",
                    "//button[contains(text(), 'Save Info')]/..//button[contains(text(), 'Not Now')]",
                    "//div[contains(text(), 'Save login info')]/..//button[contains(text(), 'Not Now')]"
                ]
                
                for selector in not_now_selectors:
                    try:
                        not_now = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        not_now.click()
                        print("✓ Dismissed 'Save Login Info' popup")
                        popup_found = True
                        # time.sleep(2)
                        break
                    except:
                        continue
            except:
                pass
            
            # Handle "Turn on Notifications" popup
            if not popup_found:
                try:
                    notification_selectors = [
                        "//button[contains(text(), 'Not Now') or contains(text(), 'Not now')]",
                        "//button[contains(text(), 'Turn on')]/..//button[contains(text(), 'Not Now')]",
                        "//div[contains(text(), 'notifications')]/..//button[contains(text(), 'Not Now')]"
                    ]
                    
                    for selector in notification_selectors:
                        try:
                            not_now = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            not_now.click()
                            print("✓ Dismissed 'Notifications' popup")
                            popup_found = True
                            time.sleep(2)
                            break
                        except:
                            continue
                except:
                    pass
            
            # Handle any other modal/popup by looking for close buttons
            if not popup_found:
                try:
                    close_selectors = [
                        "//button[@aria-label='Close']",
                        "//svg[@aria-label='Close']/..",
                        "//*[contains(@class, 'close')]",
                        "//button[contains(text(), 'Skip')]"
                    ]
                    
                    for selector in close_selectors:
                        try:
                            close_btn = WebDriverWait(self.driver, 2).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            close_btn.click()
                            print("✓ Closed modal/popup")
                            popup_found = True
                            time.sleep(2)
                            break
                        except:
                            continue
                except:
                    pass
            
            if not popup_found:
                break
            else:
                popup_attempts += 1
        
        print("✓ Popup handling completed")
    
    def login_to_instagram(self, max_attempts=3):
        """
        Complete Instagram login process
        
        Args:
            max_attempts: Maximum number of login attempts
            
        Returns:
            bool: True if login successful, False otherwise
        """
        print("Navigating to Instagram...")
        self.driver.get("https://www.instagram.com/")
        time.sleep(4)
        
        # Handle cookie consent
        self.handle_cookie_consent()
        
        # Attempt login with retries
        print("Logging in...")
        login_attempts = 0
        
        while login_attempts < max_attempts:
            login_attempts += 1
            
            if self.attempt_login():
                # Login successful, handle post-login popups
                self.handle_post_login_popups()
                return True
            else:
                print(f"Login attempt {login_attempts} failed")
                if login_attempts < max_attempts:
                    print("Refreshing page and trying again...")
                    self.driver.refresh()
                    time.sleep(4)
                else:
                    print("Max login attempts reached. Saving screenshot for debugging...")
                    self.driver.save_screenshot("login_error.png")
                    return False
        
        # Final check
        if "login" in self.driver.current_url.lower():
            print("WARNING: Still on login page after all attempts!")
            self.driver.save_screenshot("login_failed_final.png")
            print("Screenshot saved as login_failed_final.png")
            return False
        
        return True


# Convenience function for direct usage
def perform_instagram_login(driver, max_attempts=3):
    """
    Convenience function to perform Instagram login
    
    Args:
        driver: Selenium WebDriver instance
        max_attempts: Maximum number of login attempts
        
    Returns:
        bool: True if login successful, False otherwise
    """
    login_handler = InstagramLogin(driver)
    return login_handler.login_to_instagram(max_attempts)


# Example usage
if __name__ == "__main__":
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    
    # Setup driver
    options = FirefoxOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = webdriver.FirefoxService()
    driver = webdriver.Firefox(service=service, options=options)
    
    try:
        # Test login
        success = perform_instagram_login(driver)
        
        if success:
            print("✅ Login successful! You can now navigate to Instagram content.")
            time.sleep(3)  # Keep browser open to verify
        else:
            print("❌ Login failed.")
            
    except Exception as e:
        print(f"Error during login test: {e}")
    finally:
        driver.quit()