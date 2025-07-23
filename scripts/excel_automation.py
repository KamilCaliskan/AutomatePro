import pandas as pd
import os
import logging
from pathlib import Path

# 1. Configure Paths
BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "data" / "input"
OUTPUT_DIR = BASE_DIR / "data" / "output"
LOG_DIR = BASE_DIR / "logs"

# 2. Auto-create folders
for directory in [INPUT_DIR, OUTPUT_DIR, LOG_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# 3. Setup Logging
logging.basicConfig(
    filename=LOG_DIR / 'automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# 4. Handle missing input
input_file = INPUT_DIR / "sales_2023.xlsx"
output_file = OUTPUT_DIR / "report_automated.xlsx"

if not input_file.exists():
    logging.warning("⚠️ Client file missing - generating sample data")
    os.system(f"python3 {BASE_DIR / 'scripts' / 'create_sample_excel.py'}")

# 5. Data Processing with Error Handling
try:
    df = pd.read_excel(input_file)
    df["Profit"] = df["Revenue"] - df["Cost"]
    df.to_excel(output_file, index=False)
    logging.info(f"✅ Report generated: {output_file}")
except Exception as e:
    logging.error(f"🔥 Critical Error: {str(e)}")
    # TODO: Optional: notify via Slack, email, etc.
