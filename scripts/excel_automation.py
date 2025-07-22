import os
import pandas as pd

input_file = "../data/input/sales_2023.xlsx"

# 1. Dosya var mı diye kontrol et
if not os.path.exists(input_file):
    raise FileNotFoundError(
        f"❌ Client file missing: {input_file}\n"
        f"Solution: Drop Excel file into data/input/ folder"
    )

# 2. Excel dosyasını oku
df = pd.read_excel(input_file)

# 3. Veri işle (örneğin Profit sütunu ekle)
df["Profit"] = df["Revenue"] - df["Cost"]

# 4. Sonucu kaydet
output_file = "../data/output/report_automated.xlsx"
os.makedirs(os.path.dirname(output_file), exist_ok=True)  # output klasörü yoksa oluştur
df.to_excel(output_file, index=False)

print(f"✅ Report generated: {output_file}")
