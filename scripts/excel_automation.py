#!/usr/bin/env python3
"""
Enhanced Excel Automation Tool
- Cross-platform Excel processing
- Flexible column name matching
- Detailed error logging
"""

import pandas as pd
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
import unicodedata

# ====================== CONFIGURATION ======================
COLUMN_MAPPINGS: Dict[str, List[str]] = {
    'product': ['product', 'product name', 'item', 'product_name', 'product-name', 'article', 'description'],
    'sales': ['sales', 'amount', 'revenue', 'total', 'value', 'price', 'income'],
    'region': ['region', 'area', 'location', 'territory', 'zone', 'market', 'country']
}

REQUIRED_COLUMNS = {'product', 'sales'}

# ====================== LOGGING SETUP ======================
def setup_logging():
    log_file = Path(__file__).parent.parent / 'data' / 'logs' / 'excel_processing.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=str(log_file),
        filemode='a'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

# ====================== CORE FUNCTIONS ======================
def normalize_text(text: str) -> str:
    """Normalize text for reliable matching"""
    return unicodedata.normalize('NFKD', str(text).strip().lower().replace(' ', '_'))

def find_matching_column(available_columns: List[str], possible_names: List[str]) -> Optional[str]:
    """Flexible column name matching with multiple strategies"""
    try:
        available_normalized = [(col, normalize_text(col)) for col in available_columns]

        for possible in possible_names:
            possible_norm = normalize_text(possible)

            # Check for exact match first
            for orig_col, norm_col in available_normalized:
                if possible_norm == norm_col:
                    return orig_col

            # Then check for partial matches
            for orig_col, norm_col in available_normalized:
                if possible_norm in norm_col or norm_col in possible_norm:
                    return orig_col

        return None
    except Exception as e:
        logger.error(f"Column matching error: {str(e)}", exc_info=True)
        return None

def process_excel(input_file: Path, output_file: Path) -> Tuple[bool, str]:
    """Process Excel file with enhanced error handling"""
    try:
        # Try multiple engines for compatibility
        try:
            df = pd.read_excel(input_file, engine='openpyxl')
        except:
            df = pd.read_excel(input_file, engine='xlrd')

        # Build column mapping
        mapping = {}
        warnings = []
        for internal_name, possible_names in COLUMN_MAPPINGS.items():
            matched_col = find_matching_column(df.columns.tolist(), possible_names)
            if matched_col:
                mapping[internal_name] = matched_col
                logger.info(f"Column mapped: {matched_col} → {internal_name}")
            else:
                warnings.append(f"No match for '{internal_name}' (tried: {possible_names})")

        # Validate required columns
        missing = REQUIRED_COLUMNS - set(mapping.keys())
        if missing:
            error_msg = f"Missing required columns: {missing}. {'; '.join(warnings)}"
            logger.error(error_msg)
            return False, error_msg

        # Process and save data
        try:
            output_df = df.rename(columns={v:k for k,v in mapping.items()})
            output_df.to_excel(output_file, index=False, engine='openpyxl')

            success_msg = f"Successfully processed {len(df)} rows"
            logger.info(success_msg)
            return True, success_msg

        except Exception as e:
            error_msg = f"Data processing failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    except Exception as e:
        error_msg = f"File reading failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Process Excel files')
    parser.add_argument('input', help='Input Excel file path')
    parser.add_argument('output', help='Output Excel file path')
    args = parser.parse_args()

    success, message = process_excel(Path(args.input), Path(args.output))
    print(f"{'✅' if success else '❌'} {message}")
