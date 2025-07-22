# scripts/create_sample_excel.py
import pandas as pd
import os

# Sample data
data = {
    "Product": ["A", "B", "C"],
    "Revenue": [1000, 1500, 800],
    "Cost": [400, 700, 300]
}

# Ensure directory exists
os.makedirs("../data/input", exist_ok=True)

# Create sample file
output_path = "../data/input/sales_2023.xlsx"
pd.DataFrame(data).to_excel(output_path, index=False)
print(f"✅ Created sample Excel at: {output_path}")