import os
import sys
import logging
import pandas as pd
from pathlib import Path
import unicodedata
from typing import Dict, Optional, List
import traceback

# ====================== PATH HANDLING ======================
def get_base_path() -> tuple[Path, Path]:
    """
    Handle path resolution for both development and bundled versions
    Returns: (base_path, data_path)
    """
    try:
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)  # Bundled executable
        else:
            base_path = Path(__file__).parent.parent  # Development

        data_path = base_path / "data"

        # Ensure directories exist
        (data_path / "input").mkdir(parents=True, exist_ok=True)
        (data_path / "output").mkdir(parents=True, exist_ok=True)
        (data_path / "logs").mkdir(parents=True, exist_ok=True)

        return base_path, data_path

    except Exception as e:
        print(f"🚨 Critical path error: {str(e)}")
        sys.exit(1)

BASE_DIR, DATA_DIR = get_base_path()

# ====================== LOGGING SETUP ======================
log_file = DATA_DIR / "logs" / "excel_processing.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=str(log_file),
    filemode='a'
)
logger = logging.getLogger(__name__)

# ====================== CORE FUNCTIONALITY ======================
def normalize_text(text: str) -> str:
    """Normalize unicode and case for reliable matching"""
    return unicodedata.normalize('NFKD', str(text).strip()).casefold()

COLUMN_MAPPINGS: Dict[str, List[str]] = {
    'product': ['product', 'item', 'Customer', 'ürün', 'produkt', 'product name'],
    'sales': ['sales', 'amount',  'Amount', 'Satış','satış', 'umsatz', 'total', 'revenue'],
    'region': ['region','city', 'Location', 'bölge', 'gebiet', 'area', 'city', 'şehir']
}

def find_matching_column(available_columns: list, possible_names: list) -> Optional[str]:
    """
    Find matching column with flexible naming
    Returns: matched column name or None
    """
    try:
        available_normalized = [(col, normalize_text(col)) for col in available_columns]
        for possible in possible_names:
            possible_normalized = normalize_text(possible)
            for orig_col, norm_col in available_normalized:
                if possible_normalized in norm_col or norm_col in possible_normalized:
                    return orig_col
        return None
    except Exception as e:
        logger.error(f"Column matching failed: {str(e)}", exc_info=True)
        return None
def validate_columns(df):
    missing = []
    for col in ['product', 'sales']:
        if col not in df.columns:
            missing.append(col)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def process_excel(input_file: Path, output_file: Path) -> bool:
    """
    Process Excel file with error handling
    Returns: True if successful, False otherwise
    """
    try:
        logger.info(f"🔍 Starting processing: {input_file}")

        # Read input with engine detection
        try:
            df = pd.read_excel(input_file, engine=None)
            logger.info(f"📊 Loaded DataFrame with columns: {list(df.columns)}")
        except Exception as e:
            logger.error(f"Failed to read Excel file: {str(e)}")
            return False

        # Build column mapping
        mapping = {}
        for internal_name, possible_names in COLUMN_MAPPINGS.items():
            matched_col = find_matching_column(df.columns, possible_names)
            if matched_col:
                mapping[internal_name] = matched_col
                logger.info(f"🔗 Mapped '{matched_col}' → '{internal_name}'")
            else:
                logger.warning(f"⚠️ No match for {internal_name}")

        # Validate essential columns
        required_columns = {'product', 'sales'}
        if not required_columns.issubset(mapping.keys()):
            missing = required_columns - set(mapping.keys())
            raise ValueError(f"Missing required columns: {missing}")

        # Process data with row-level error handling
        processed_data = []
        error_count = 0

        for idx, row in df.iterrows():
            try:
                processed_data.append({
                    'product': str(row[mapping['product']]).strip(),
                    'sales': round(float(row[mapping['sales']]), 2),
                    'region': str(row.get(mapping.get('region', ''), 'Unknown')).strip(),
                    'source_row': idx + 2
                })
            except Exception as e:
                error_count += 1
                logger.warning(f"⚠️ Row {idx+2} skipped: {str(e)}")
                continue

        # Save output
        try:
            pd.DataFrame(processed_data).to_excel(
                output_file,
                index=False,
                engine='openpyxl'
            )
            logger.info(f"✅ Success! Output saved to {output_file}")
            if error_count > 0:
                logger.warning(f"⚠️ Skipped {error_count} rows with errors")
            return True

        except Exception as e:
            logger.error(f"Failed to save output: {str(e)}")
            return False

    except Exception as e:
        logger.error(f"❌ Processing failed: {str(e)}", exc_info=True)
        print(f"🔥 FAIL REASON: {str(e)}" if 'e' in locals() else "🔥 UNKNOWN FAILURE")
        return False  # ← Final return point

# ====================== COMMAND LINE INTERFACE ======================
def main() -> int:
    """Command line entry point"""
    parser = argparse.ArgumentParser(
        description='AutomatePro Excel Processor v2.5',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        'input',
        help='Input file name (from data/input/)'
    )
    parser.add_argument(
        'output',
        help='Output file name (saved to data/output/)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed console output'
    )

    args = parser.parse_args()

    # Configure paths
    input_file = DATA_DIR / "input" / args.input
    output_file = DATA_DIR / "output" / args.output

    # Validate input
    if not input_file.exists():
        print(f"❌ Error: Input file not found at {input_file}")
        return 1

    # Process file
    success = process_excel(input_file, output_file)

    # Output results
    if success:
        print(f"✅ Success! Output saved to:\n{output_file}")
        if args.verbose:
            print(f"📄 Log file: {log_file}")
        return 0
    else:
        print(f"❌ Processing failed - check logs:\n{log_file}")
        return 1

if __name__ == "__main__":
    import argparse
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"🚨 Unexpected error: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
