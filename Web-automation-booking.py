from seleniumbase import BaseCase
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import logging
import time
import os
import tempfile

# Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Proxy configuration
proxy_host = "geo.iproyal.com"
proxy_port = "12321"
proxy_username = "zVO94b9ZpCtswL7K"
proxy_password = "Zb3Mp8F8rpsMNIXI_session-8Qetgtt9_lifetime-59m_streaming-1"

# Manifest JSON and Background JS content
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version": "22.0.0"
}
"""

background_js = """
var config = {
    mode: "fixed_servers",
    rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
""".strip() % (proxy_host, proxy_port, proxy_username, proxy_password)

class WebBookingAutomation(BaseCase):
    def setUp(self):
        # Create a temporary directory to store the extension files
        self.temp_dir = tempfile.mkdtemp()

        # Write manifest.json and background.js to the temporary directory
        with open(os.path.join(self.temp_dir, 'manifest.json'), 'w') as manifest_file:
            manifest_file.write(manifest_json)
        
        with open(os.path.join(self.temp_dir, 'background.js'), 'w') as background_file:
            background_file.write(background_js)
        
        # Set Chrome options for undetected_chromedriver
        self.options = Options()
        self.options.add_argument(f"--load-extension={self.temp_dir}")
        self.options.add_experimental_option("debuggerAddress", "localhost:8989")
        self.options.add_argument("--headless")  # Run in headless mode
        self.options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration
        self.options.add_argument("--no-sandbox")  # Disable sandboxing
        self.options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems

        # Initialize undetected Chrome driver with the configured options
        self.driver = uc.Chrome(service=Service(), options=self.options)
        self.driver.set_window_size(1920, 1080)
        super().setUp()

    def test_login(self):
        logging.info("Opening the target URL...")
        self.driver.get('https://visa.vfsglobal.com/cpv/pt/prt/login')

        # Allow time for the extension to authenticate the proxy
        logging.info("Waiting for the page to load and the extension to authenticate...")
        time.sleep(10)

        # Decline cookies if the cookie banner appears
        try:
            logging.info("Attempting to decline cookies...")
            reject_all_button = self.driver.find_element(By.ID, 'onetrust-reject-all-handler')
            reject_all_button.click()
            logging.info("Cookies declined.")
        except Exception as e:
            logging.warning(f"Cookie decline button not found: {e}")

        # Input credentials into the form
        Username = "test@marca.33mail.com"
        Password = "Test@2121"

        try:
            # Locate the username input and enter the username
            logging.info("Entering username...")
            self.driver.find_element(By.ID, 'email').send_keys(Username)
            
            # Locate the password input and enter the password
            logging.info("Entering password...")
            self.driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(Password)
            
            # Take a screenshot after interaction
            self.driver.save_screenshot("after_interaction.png")
            logging.info("Screenshot taken after interacting with the form.")

            # Click the element with the text "Verify you are human"
            logging.info("Attempting to click the 'Verify you are human' span...")
            verify_element = self.driver.find_element(By.XPATH, "//span[text()='Verify you are human']")
            verify_element.click()
            logging.info("'Verify you are human' span clicked.")

            # Pause to handle any potential CAPTCHA
            time.sleep(5)
            self.driver.save_screenshot("captcha.png")

        except Exception as e:
            logging.error(f"An error occurred during form interaction: {e}")
            self.driver.save_screenshot("error_screenshot.png")

    def tearDown(self):
        # Clean up the temporary directory
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
        
        # Prevent the browser from quitting immediately
        input("Press Enter to quit the browser...")
        self.driver.quit()
        super().tearDown()
        logging.info("Driver session ended.")

if __name__ == "__main__":
    BaseCase.main(__name__, __file__)
