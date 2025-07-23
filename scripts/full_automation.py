from crm_scraper import scrape_shitty_crm
from excel_automation import process_excel
import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting full automation")
    
    # 1. Scrape CRM
    try:
        crm_data = scrape_shitty_crm()
        logging.info(f"Scraped {len(crm_data)} customers")
    except Exception as e:
        logging.error(f"CRM failed: {str(e)}")
        crm_data = None
    
    # 2. Process Excel (even if CRM failed)
    process_excel()
    
    # 3. Optional: Email results
    if crm_data is not None:
        logging.info("Sending email to client...")
        # Add email code here

if __name__ == "__main__":
    main()