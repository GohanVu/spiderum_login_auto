from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import getpass
import os
import pickle
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("instagram_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("InstagramAutomation")

class InstagramBot:
    def __init__(self, headless=False):
        self.driver = None
        self.headless = headless
        self.cookies_file = "instagram_cookies.pkl"
    
    def setup_driver(self):
        """Set up and configure the Chrome WebDriver"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--start-maximized")
        
        # Create browser instance
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Browser initialized")
    
    def load_cookies(self):
        """Load cookies from file if available"""
        if os.path.exists(self.cookies_file):
            try:
                self.driver.get("https://www.instagram.com")
                cookies = pickle.load(open(self.cookies_file, "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                logger.info("Cookies loaded successfully")
                return True
            except Exception as e:
                logger.error(f"Error loading cookies: {e}")
        return False
    
    def save_cookies(self):
        """Save current cookies to file"""
        try:
            cookies = self.driver.get_cookies()
            pickle.dump(cookies, open(self.cookies_file, "wb"))
            logger.info("Cookies saved successfully")
        except Exception as e:
            logger.error(f"Error saving cookies: {e}")
    
    def handle_cookies_notice(self):
        """Handle the cookies consent popup if it appears"""
        try:
            cookie_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            cookie_button.click()
            logger.info("Accepted cookies")
        except:
            logger.info("No cookie notice found or already accepted")
    
    def login(self, username=None, password=None, use_cookies=True):
        """Login to Instagram"""
        if not self.driver:
            self.setup_driver()
        
        # First try with cookies if enabled
        cookies_worked = False
        if use_cookies:
            cookies_worked = self.load_cookies()
            if cookies_worked:
                self.driver.get("https://www.instagram.com")
                time.sleep(3)
                # Check if we're actually logged in
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Search')]"))
                    )
                    logger.info("Login successful using cookies!")
                    return True
                except:
                    logger.info("Cookie login failed, will try with credentials")
                    cookies_worked = False
        
        if not cookies_worked:
            # Regular login with credentials
            self.driver.get("https://www.instagram.com/accounts/login/")
            logger.info("Accessing Instagram login page...")
            
            # Handle cookie notice
            self.handle_cookies_notice()
            
            # Wait for the login form to load
            try:
                username_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
                )
                
                # Get username and password if not provided
                if not username:
                    username = input("Enter your Instagram username: ")
                if not password:
                    password = getpass.getpass("Enter your Instagram password: ")
                
                # Enter username
                username_input.send_keys(username)
                
                # Enter password
                password_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")
                password_input.send_keys(password)
                
                # Click login button
                login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                login_button.click()
                
                logger.info("Login credentials submitted")
                
                # Wait for login to complete
                try:
                    WebDriverWait(self.driver, 15).until(
                        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Search')]"))
                    )
                    logger.info("Login successful!")
                    # Save cookies for future logins
                    self.save_cookies()
                    return True
                except TimeoutException:
                    # Check for verification required
                    try:
                        if "verification" in self.driver.page_source.lower() or "challenge" in self.driver.page_source.lower():
                            logger.warning("Additional verification required. Please complete it manually.")
                            input("Press Enter after completing verification...")
                            self.save_cookies()
                            return True
                    except:
                        pass
                    
                    logger.error("Login failed")
                    return False
                
            except Exception as e:
                logger.error(f"Login error: {e}")
                return False
    
    def search_user(self, username):
        """Search for a user on Instagram"""
        try:
            # Click on search
            search_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Search')]"))
            )
            search_button.click()
            
            # Enter search query
            search_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Search']"))
            )
            search_input.clear()
            search_input.send_keys(username)
            
            # Wait for search results
            time.sleep(2)
            
            # Click on the first result
            search_results = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{username}')]"))
            )
            search_results.click()
            
            logger.info(f"Navigated to user: {username}")
            return True
        except Exception as e:
            logger.error(f"Error searching for user: {e}")
            return False
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the current page"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"instagram_screenshot_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved as {filename}")
            return True
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
            self.driver = None

def main():
    print("Instagram Automation Bot - Advanced Example")
    print("-------------------------------------------")
    
    bot = InstagramBot(headless=False)
    
    try:
        # Login
        login_successful = bot.login()
        
        if login_successful:
            # Demonstrate additional features
            print("\nWhat would you like to do?")
            print("1. Search for a user")
            print("2. Take a screenshot")
            print("3. Exit")
            
            choice = input("Enter your choice (1-3): ")
            
            if choice == "1":
                username = input("Enter Instagram username to search: ")
                bot.search_user(username)
                time.sleep(5)
                bot.take_screenshot(f"{username}_profile.png")
            
            elif choice == "2":
                filename = input("Enter filename for screenshot (or press Enter for auto-generated name): ")
                if filename.strip() == "":
                    filename = None
                bot.take_screenshot(filename)
        
        input("\nPress Enter to close the browser...")
    
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    
    finally:
        bot.close()

if __name__ == "__main__":
    main() 