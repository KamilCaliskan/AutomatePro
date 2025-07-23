# scripts/excel_automation.py
import pandas as pd
import os
from pathlib import Path

def process_excel(input_path, output_path):
    """Process Excel file and save with Profit column"""
    try:
        df = pd.read_excel(input_path)
        df["Profit"] = df["Revenue"] - df["Cost"]
        df.to_excel(output_path, index=False)
        print(f"✅ Excel report generated: {output_path}")
        return True
    except Exception as e:
        print(f"🔥 Excel Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Auto-create folders if missing
    BASE_DIR = Path(__file__).parent.parent
    input_file = BASE_DIR / "data" / "input" / "sales_2023.xlsx"
    output_file = BASE_DIR / "data" / "output" / "report_automated.xlsx"
    
    input_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    process_excel(input_file, output_file)