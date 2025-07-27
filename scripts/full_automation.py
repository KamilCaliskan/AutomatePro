import os
import logging
from pathlib import Path
from excel_automation import process_excel
from crm_scraper import scrape_crm

# 🔧 Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=Path(__file__).parent.parent / 'logs' / 'automation.log'
)

def main():
    BASE_DIR = Path(__file__).parent.parent
    input_path = BASE_DIR / "data" / "input" / "sales_2023.xlsx"

    # ✅ Path Verification
    if not input_path.exists():
        logging.warning("⚠️ Nuclear option: Regenerating sample data")
        os.system("python3 scripts/create_sample_excel.py")

    # 1. 📊 Process Excel
    excel_success = process_excel(
        input_path=input_path,
        output_path=BASE_DIR / "data" / "output" / "report_automated.xlsx"
    )

    # 2. 🌐 Scrape CRM
    scrape_crm()

    # 3. ✉️ Optional: Add email notification

if __name__ == "__main__":
    main()
