from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import json
import logging

# Get the current timestamp
start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'test_results_{start_time}.log'

# Set up logging with dynamic file name
logging.basicConfig(filename=log_filename, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')


options = ChromeOptions();
options.add_argument("--disable-search-engine-choice-screen");
options.add_argument('--ignore-ssl-errors=yes');
options.add_argument('--ignore-certificate-errors');
options.set_capability('sessionName', 'BStack test Safari')
driver = webdriver.Remote(
    command_executor='https://xxxx',
    options=options)

base_url = 'https://demo.invibes.com/2022/refinery29.html?BVID=';
valuesBvid = ['32', '34', '794022'];

executor_object = {
    'action': 'setSessionName',
    'arguments': {
        'name': "<Test Safari>"
    }
}
browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
driver.execute_script(browserstack_executor)

for value in valuesBvid:
    full_url = base_url + value;
    driver.get(full_url);

    time.sleep(1);

    #scroll to divIvbs
    attempts = 0
    while attempts < 3:
        try: 
            divIvbs = driver.find_element(By.ID, "divIvbsInfeed");
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", divIvbs);
            time.sleep(1)
            if divIvbs:
            # Set the status of test as 'passed' if div was found
                driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "DivIvbs was found and scrolled to"}}')
                time.sleep(1)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename_save = f'c:/xxxx/Safari18Beta&BVID={value}&timestamp={timestamp}.png'
             # Capture the screenshot with the generated filename
                driver.save_screenshot(filename_save);
                logging.info(f'Test passed for BVID={value}. Screenshot saved as {filename_save}')
                break  # Exit the loop if successful

        except NoSuchElementException:
            print("divIvbs not found");
            # Set the status of test as 'failed' if div was not found
            driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "DivIvbs was NOT found and scrolled to"}}')
            driver.refresh();
            time.sleep(2);
            attempts += 1  # Increment the attempts counter
            if attempts == 3:
                logging.error(f'Test failed for BVID={value}. DivIvbs not found after 3 attempts.')

    time.sleep(1);

driver.quit();