import pandas as pd
from pathlib import Path
import logging

def create_sample_data():
    """Generates sample Excel file with dummy data. Ensures directories exist."""
    BASE_DIR = Path(__file__).parent.parent
    output_path = BASE_DIR / "data" / "input" / "sales_2023.xlsx"

    # ✅ Ensure the output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 🧪 Sample data
    data = {
        "Product": ["A", "B", "C"],
        "Revenue": [1000, 1500, 800],
        "Cost": [400, 700, 300]
    }

    # 💾 Write to Excel
    pd.DataFrame(data).to_excel(output_path, index=False)
    logging.info(f"✅ Sample data created at: {output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
    create_sample_data()
