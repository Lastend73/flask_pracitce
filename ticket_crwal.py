from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no browser UI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--no-sandbox")  # Bypass OS security model

# Set up the Chrome driver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Example URL to crawl
url = 'https://example.com'

# Open the URL
driver.get(url)

# Wait for the page to load
time.sleep(3)

element = driver.find_element(By.NAME, 'q')  # Update with the actual element you want to interact with
element.send_keys('example search' + Keys.RETURN)

# Wait for the results to load
time.sleep(3)

# Close the browser
driver.quit()