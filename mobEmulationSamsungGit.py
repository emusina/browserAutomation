from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import logging
from datetime import datetime
import time

# Define the mobile emulation settings for Samsung Galaxy A51
mobile_emulation = {
    "deviceMetrics": { "width": 412, "height": 915, "pixelRatio": 2.625 },
    "userAgent": "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"
}

# Get the current timestamp
start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'c:/xxxx/test_results_{start_time}.log'

# Set up logging with dynamic file name
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

options = ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument("--disable-search-engine-choice-screen")
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(options=options)

#define the url to load and the BVIDs array
base_url = 'https://demo.xxxx.com/page.html?BVID='
valuesBvid = ['32', '34', '794022']

for value in valuesBvid:
    full_url = base_url + value
    driver.get(full_url)

    time.sleep(1)

    # Scroll to divIvbs
    attempts = 0
    while attempts < 3:
        try:
            divIvbs = driver.find_element(By.ID, "divIvbsInfeed")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", divIvbs)
            time.sleep(1)
            if divIvbs:
                # Step 1: Find and click the element with class "ivTrigger"
                iv_trigger = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ivTrigger"))
                )
                iv_trigger.click()

                # Step 2: Wait until the class changes to "ivTrigger active"
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ivTrigger.active"))
                )

                # Step 3: Click the element with class "ivCookiesO ivCookies"
                iv_cookies = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "ivCookiesO.ivCookies"))
                )
                iv_cookies.click()
                time.sleep(2)
                # Log the status of test as 'passed' if div was found
                logging.info(f'Test passed for BVID={value}. DivIvbs was found, scrolled to, and clicked on Cookie Menu.')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename_save = f'c:/xxxx/ChromeMobEmulation&BVID={value}&timestamp={timestamp}.png'
               
                # Capture the screenshot with the generated filename
                driver.save_screenshot(filename_save)
                logging.info(f'Screenshot saved as {filename_save}')
                break  # Exit the loop if successful
        except NoSuchElementException:
            print("divIvbs not found")
            # Log the status of test as 'failed' if div was not found
            logging.error(f'Test failed for BVID={value}. DivIvbs not found.')
            driver.refresh()
            time.sleep(2)
            attempts += 1  # Increment the attempts counter
            if attempts == 3:
                logging.error(f'Test failed for BVID={value}. DivIvbs not found after 3 attempts.')

    time.sleep(1)

driver.quit()
