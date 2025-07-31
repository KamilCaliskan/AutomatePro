import os
import sys
import logging
import pandas as pd
from pathlib import Path
import unicodedata
from typing import Dict, Optional

# ====================== PATH HANDLING ======================
def get_base_path():
    """Handle path resolution for both development and bundled versions"""
    if getattr(sys, 'frozen', False):
        # Running as bundled executable
        base_path = Path(sys._MEIPASS)
        data_path = base_path / "data"
    else:
        # Running in development
        base_path = Path(__file__).parent.parent
        data_path = base_path / "data"

    # Create data directories if they don't exist
    (data_path / "input").mkdir(parents=True, exist_ok=True)
    (data_path / "output").mkdir(parents=True, exist_ok=True)
    (data_path / "logs").mkdir(parents=True, exist_ok=True)

    return base_path, data_path

BASE_DIR, DATA_DIR = get_base_path()

# ====================== LOGGING SETUP ======================
log_file = DATA_DIR / "logs" / "excel_processing.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(log_file)
)

# ====================== MAIN FUNCTIONALITY ======================
def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFKD', str(text).strip()).casefold()

COLUMN_MAPPINGS = {
    'product': ['product', 'item', 'ürün adı', 'product name'],
    'sales': ['sales', 'amount', 'satış miktarı', 'totalprice'],
    'region': ['region', 'shippingaddress', 'bölge', 'city']
}

def find_matching_column(available_columns: list, possible_names: list) -> Optional[str]:
    available_normalized = [(col, normalize_text(col)) for col in available_columns]
    for possible in possible_names:
        possible_normalized = normalize_text(possible)
        for orig_col, norm_col in available_normalized:
            if possible_normalized in norm_col or norm_col in possible_normalized:
                return orig_col
    return None

def process_excel(input_file: Path, output_file: Path) -> bool:
    try:
        logging.info(f"Processing started: {input_file}")

        # Read input
        df = pd.read_excel(input_file)

        # Column mapping
        mapping = {}
        for internal_name, possible_names in COLUMN_MAPPINGS.items():
            matched_col = find_matching_column(df.columns, possible_names)
            if matched_col:
                mapping[internal_name] = matched_col
                logging.info(f"Mapped '{matched_col}' → '{internal_name}'")

        # Validate columns
        if not {'product', 'sales'}.issubset(mapping.keys()):
            raise ValueError("Missing required columns (product and sales)")

        # Process data
        processed_data = []
        for idx, row in df.iterrows():
            try:
                processed_data.append({
                    'product': str(row[mapping['product']]).strip(),
                    'sales': round(float(row[mapping['sales']]), 2),
                    'region': str(row.get(mapping.get('region', ''), 'Unknown')).strip(),
                    'source_row': idx + 2
                })
            except Exception as e:
                logging.error(f"Row {idx+2} error: {str(e)}")
                continue

        # Save output
        pd.DataFrame(processed_data).to_excel(output_file, index=False)
        logging.info(f"Successfully saved to {output_file}")
        return True

    except Exception as e:
        logging.error(f"Processing failed: {str(e)}", exc_info=True)
        return False

# ====================== COMMAND LINE INTERFACE ======================
def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process Excel files')
    parser.add_argument('input', help='Input file name (in data/input/)')
    parser.add_argument('output', help='Output file name (in data/output/)')
    args = parser.parse_args()

    input_file = DATA_DIR / "input" / args.input
    output_file = DATA_DIR / "output" / args.output

    if not input_file.exists():
        print(f"Error: Input file not found at {input_file}")
        return 1

    success = process_excel(input_file, output_file)
    if success:
        print(f"✅ Success! Output saved to {output_file}")
        return 0
    else:
        print("❌ Processing failed - check logs for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())
