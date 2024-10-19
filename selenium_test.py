from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import logging
import time

logging.basicConfig(
    filename='logs/test_log.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

driver = webdriver.Safari()
# Maximize the Safari window
driver.maximize_window()

try:
    logging.info("Opening ThinkTribe homepage...")
    driver.get("https://thinktribe.com")

    WebDriverWait(driver, 10).until(
        EC.title_contains("Reduce online abandonment")
    )
    logging.info(f"Homepage title: {driver.title}")
    time.sleep(1)
    driver.save_screenshot('screenshots/homepage_initial.png')

    try:
        cookie_ok_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyLevelButtonAccept"))
        )
        cookie_ok_button.click()
        logging.info("Cookie banner dismissed.")
    except Exception as e:
        logging.warning(f"Failed to dismiss cookie banner: {e}")

    time.sleep(1)
    driver.save_screenshot('screenshots/homepage_after_cookie.png')

    # Define services to navigate
    services = [
        ("Mobile DCX Intelligence", "https://thinktribe.com/mobile-performance-monitoring/"),
        ("Native App DCX Intelligence", "https://thinktribe.com/native-app-monitoring-on-android-ios/"),
        ("Load & Performance Testing", "https://thinktribe.com/load-and-performance-testing/"),
        ("DCX Release Testing", "https://thinktribe.com/release-acceptance-testing/"),
        ("DCX Audit", "https://thinktribe.com/site-audit/")
    ]

    # Loop through each service
    for service_name, service_url in services:
        try:
            # Hover over the Services menu to display the dropdown
            services_menu = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Services"))
            )
            ActionChains(driver).move_to_element(services_menu).perform()
            time.sleep(1)  # Short wait to ensure dropdown is visible

            service_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, service_name))
            )
            service_link.click()
            logging.info(f"{service_name} link clicked.")
            time.sleep(2)  # Slightly longer wait for page to load

            driver.save_screenshot(f'screenshots/{service_name.replace(" ", "_").lower()}_screenshot.png')

            WebDriverWait(driver, 10).until(
                EC.url_contains(service_url)
            )
            logging.info(f"Successfully navigated to {service_name} page.")

        except Exception as e:
            logging.error(f"Error navigating to {service_name}: {e}")

finally:
    logging.info("Closing the browser...")
    driver.quit()

