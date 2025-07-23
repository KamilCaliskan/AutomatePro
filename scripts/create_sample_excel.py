import pandas as pd
from pathlib import Path

def create_sample_data():
    BASE_DIR = Path(__file__).parent.parent
    output_path = BASE_DIR / "data" / "input" / "sales_2023.xlsx"
    
    # Create sample data
    data = {
        "Product": ["A", "B", "C"],
        "Revenue": [1000, 1500, 800],
        "Cost": [400, 700, 300]
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(data).to_excel(output_path, index=False)
    print(f"✅ Sample data created: {output_path}")

if __name__ == "__main__":
    create_sample_data()