from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os
from pathlib import Path

def scrape_crm():
    """Scrape CRM data and save to Excel"""
    BASE_DIR = Path(__file__).parent.parent
    output_file = BASE_DIR / "data" / "output" / "crm_data.xlsx"
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run silently
        driver = webdriver.Chrome(options=options)
        
        # Example CRM - REPLACE WITH CLIENT'S URL
        driver.get("http://example-crm.com/login")
        time.sleep(2)
        
        # Mock login - ADAPT TO CLIENT'S CRM
        driver.find_element(By.ID, "username").send_keys("demo")
        driver.find_element(By.ID, "password").send_keys("demo123")
        driver.find_element(By.XPATH, "//button[contains(text(),'Login')]").click()
        time.sleep(3)
        
        # Mock data extraction
        data = []
        rows = driver.find_elements(By.XPATH, "//table[@id='customers']/tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                data.append({
                    "Name": cells[0].text,
                    "Email": cells[1].text,
                    "Last_Purchase": cells[2].text
                })
        
        pd.DataFrame(data).to_excel(output_file, index=False)
        print(f"✅ CRM data saved: {output_file}")
        
    except Exception as e:
        print(f"🔥 CRM Error: {str(e)}")
        # Save screenshot for debugging
        driver.save_screenshot(str(BASE_DIR / "data" / "crm_error.png"))
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_crm()