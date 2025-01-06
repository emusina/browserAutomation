from playwright.sync_api import sync_playwright
import re
import logging
from datetime import datetime

# Logging setup
start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'D:/xxxx/BrowserAutomation/Logs/test_results_{start_time}.log'
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a function to capture network requests
def capture_network_logs(page, pattern):
    logs = []

    # Updated to add debugging for all network responses
    def handle_response(response):
        url = response.url
        logging.debug(f"Response URL: {url}")  # Log every URL for debugging
        if re.search(pattern, url):
            logs.append(url)
            logging.info(f"Captured URL: {url}")
    
    page.on("response", handle_response)
    return logs

# Define the main function
def main():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)  # Set headless=True for headless mode
        context = browser.new_context(
            viewport={"width": 412, "height": 915},
            user_agent="Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36"
        )
        page = context.new_page()

        # Define the base URL and BVIDs
        base_url = 'https://demo.xxxx.com/page.html?BVID='
        valuesBvid = ['32']
        pattern = r'.xxxx/Stat/gb.json.*1051'

        for value in valuesBvid:
            full_url = base_url + value
            logging.info(f"Loading URL: {full_url}")

            # Start capturing network logs BEFORE navigating
            logs = capture_network_logs(page, pattern)

            # Navigate to the URL
            page.goto(full_url)

            # Add a wait to ensure network requests are captured
            page.wait_for_timeout(2000)  # Wait 5 seconds for any network requests

            # Scroll to the ad
            try:
                page.wait_for_selector("#divIvbsInfeed", timeout=5000)
                div_ivbs = page.locator("#divIvbsInfeed")
                div_ivbs.scroll_into_view_if_needed()

                # Wait a bit more for additional network requests
                page.wait_for_timeout(4000)

                # Perform actions (click on ad)
                iv_trigger = page.locator(".ivTrigger")
                iv_trigger.click()
                page.wait_for_selector(".ivTrigger.active", timeout=5000)

                # Click on cookie menu
                iv_cookies = page.locator(".ivCookiesO.ivCookies")
                iv_cookies.click()

                # Capture screenshot
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                page.screenshot(path=f"screenshot_{value}_{timestamp}.png")
            except Exception as e:
                logging.error(f"Error during processing BVID={value}: {e}")

        # Log captured URLs after all processing
        logging.info("Captured network logs:")
        for log in logs:
            logging.info(log)

        browser.close()

# Run the main function
main()
