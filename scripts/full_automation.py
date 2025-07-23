from excel_automation import process_excel
from crm_scraper import scrape_crm
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=Path(__file__).parent.parent / 'logs' / 'automation.log'
)

def main():
    BASE_DIR = Path(__file__).parent.parent
    
    # 1. Process Excel
    excel_success = process_excel(
        input_path=BASE_DIR / "data" / "input" / "sales_2023.xlsx",
        output_path=BASE_DIR / "data" / "output" / "report_automated.xlsx"
    )
    
    # 2. Scrape CRM
    scrape_crm()
    
    # 3. Optional: Add email notification here

if __name__ == "__main__":
    main()