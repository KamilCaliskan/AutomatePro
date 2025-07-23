from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import pandas as pd
import time
from pathlib import Path
import logging

# 1. Setup Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "output"
ERROR_DIR = BASE_DIR / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
ERROR_DIR.mkdir(parents=True, exist_ok=True)

# 2. Setup Logging
LOG_PATH = BASE_DIR / "logs" / "crm_scraper.log"
LOG_PATH.parent.mkdir(exist_ok=True)
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def scrape_shitty_crm():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1200,800")
    # options.add_argument("--headless")  # Uncomment for silent mode
    
    try:
        driver = webdriver.Chrome(options=options)
        logging.info("🚀 Browser launched successfully.")
    except WebDriverException as e:
        logging.error(f"❌ Failed to launch browser: {str(e)}")
        return

    try:
        # 3. Login
        driver.get("http://client-crm.de/login")
        driver.find_element(By.ID, "username").send_keys("admin")
        driver.find_element(By.ID, "password").send_keys("password123")
        driver.find_element(By.XPATH, "//input[@type='submit']").click()
        logging.info("🔐 Logged into CRM")
        time.sleep(3)

        # 4. Scrape Data
        customers = []
        rows = driver.find_elements(By.XPATH, "//table[@id='customers']/tbody/tr")

        if not rows:
            raise NoSuchElementException("No rows found in customer table.")

        for row in rows:
            customers.append({
                "name": row.find_element(By.XPATH, "./td[1]").text,
                "email": row.find_element(By.XPATH, "./td[2]").text,
                "last_purchase": row.find_element(By.XPATH, "./td[3]").text
            })

        # 5. Save to Excel
        df = pd.DataFrame(customers)
        output_path = OUTPUT_DIR / "crm_customers.xlsx"
        df.to_excel(output_path, index=False)
        logging.info(f"✅ CRM data exported to: {output_path}")
        print(f"✅ Data saved to {output_path}")
        return df

    except NoSuchElementException as e:
        screenshot_path = ERROR_DIR / "error_screenshot.png"
        driver.save_screenshot(str(screenshot_path))
        logging.error(f"🔥 CRM HTML changed or missing element: {str(e)}")
        logging.info(f"📸 Screenshot saved at: {screenshot_path}")
        print("🔥 Critical error occurred. Check log and screenshot.")
        raise

    except Exception as e:
        logging.error(f"💥 Unexpected error: {str(e)}")
        raise

    finally:
        driver.quit()
        logging.info("🧹 Browser session ended.")

if __name__ == "__main__":
    scrape_shitty_crm()
