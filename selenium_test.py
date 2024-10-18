from selenium import webdriver  # WebDriver interface for browser control
from selenium.webdriver.common.by import By  # Locators strategy
from selenium.webdriver.support.ui import WebDriverWait  # Explicit waits
from selenium.webdriver.support import expected_conditions as EC  # Wait conditions
from selenium.webdriver.chrome.service import Service  # ChromeDriver service handling
from selenium.common.exceptions import TimeoutException, WebDriverException  # Exception handling
import logging  # Logging to track events
import time  # Time module for sleep delays

# Set up logging
logging.basicConfig(
    filename='logs/test_log.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize WebDriver with ChromeOptions
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximize window to avoid scaling issues
driver = webdriver.Chrome(options=options)

try:
    logging.info("Opening ThinkTribe homepage...")
    driver.get("https://thinktribe.com")

    # Wait until the homepage loads completely by checking the title
    WebDriverWait(driver, 10).until(
        EC.title_contains("Reduce online abandonment")
    )
    logging.info(f"Homepage title: {driver.title}")

    # Handle cookie banner
    try:
        cookie_ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonAccept"))
        )
        cookie_ok_button.click()
        logging.info("Cookie banner dismissed.")
    except Exception as e:
        logging.warning(f"Failed to dismiss cookie banner: {e}")

    # Open 'Services' dropdown
    services_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Services"))
    )
    services_menu.click()
    logging.info("'Services' dropdown opened.")

    # Click 'DCX Intelligence' link
    dcx_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "DCX Intelligence"))
    )
    dcx_link.click()
    logging.info("'DCX Intelligence' link clicked.")

    # Wait until the new page fully loads by monitoring the URL
    WebDriverWait(driver, 10).until(
        EC.url_contains("website-performance-monitoring")
    )

    # Adding delay to ensure all elements render before taking the screenshot
    time.sleep(5)  # Wait an additional 5 seconds

    # Save the final screenshot
    driver.save_screenshot('screenshots/final_screenshot.png')
    logging.info("Saving final screenshot...")

finally:
    logging.info("Closing the browser...")
    driver.quit()

