# 🚀 AutomatePro - Excel Automation Tool

<div align="right">
  <a href="#english">English</a> | 
  <a href="#turkish">Türkçe</a> | 
  <a href="#german">Deutsch</a>
</div>

---

## 🌟 Features Overview / Özellikler / Funktionen
| 🇬🇧 English               | 🇹🇷 Türkçe                 | 🇩🇪 Deutsch               |
|--------------------------|--------------------------|--------------------------|
| AI-powered Excel processing | Excel işleme (AI destekli) | Excel-Verarbeitung (KI) |
| Multi-language support    | Çoklu dil desteği        | Mehrsprachiger Support   |
| Address parsing           | Adres ayrıştırma         | Adressanalyse            |

---

<a name="english"></a>
## 🇬🇧 English Documentation

### 📦 Installation
```bash
git clone https://github.com/KamilCaliskan/AutomatePro.git
cd AutomatePro
pip install -r requirements.txt

🛠️ Usage

# Process Excel files
python scripts/excel_automation.py input.xlsx output.xlsx

# Create executable
pyinstaller --onefile --add-data "data/:data" scripts/excel_automation.py

🧩 Features

    Automatic column mapping

    Support for 50+ column name variants

    Detailed error logging

<a name="turkish"></a>
🇹🇷 Türkçe Dokümantasyon
📦 Kurulum

git clone https://github.com/KamilCaliskan/AutomatePro.git
cd AutomatePro
pip install -r requirements.txt

🛠️ Kullanım

# Excel dosyalarını işleme
python scripts/excel_automation.py girdi.xlsx çıktı.xlsx

# Çalıştırılabilir dosya oluşturma
pyinstaller --onefile --add-data "data/:data" scripts/excel_automation.py

🧩 Özellikler

    Otomatik sütun eşleme

    50+ farklı sütun ismi desteği

    Detaylı hata kayıtları

<a name="german"></a>
🇩🇪 Deutsche Dokumentation
📦 Installation

git clone https://github.com/KamilCaliskan/AutomatePro.git
cd AutomatePro
pip install -r requirements.txt

🛠️ Verwendung

# Excel-Dateien verarbeiten
python scripts/excel_automation.py eingabe.xlsx ausgabe.xlsx

# Ausführbare Datei erstellen
pyinstaller --onefile --add-data "data/:data" scripts/excel_automation.py

🧩 Funktionen

    Automatische Spaltenzuordnung

    Unterstützung für 50+ Spaltennamen

    Detaillierte Fehlerprotokollierung

🛠 Technical Setup / Teknik Kurulum / Technische Einrichtung
🐍 Python Requirements

# Common for all languages
COLUMN_MAPPINGS = {
    'product': ['product', 'ürün', 'produkt'],
    'sales': ['sales', 'satış', 'umsatz']
}

📂 Directory Structure / Dizin Yapısı / Verzeichnisstruktur

AutomatePro/
├── data/           # Input/Output files | Girdi/Çıktı | Eingabe/Ausgabe
│   ├── input/      # Excel files to process | İşlenecek dosyalar | Zu verarbeitende Dateien
│   └── output/     # Processed results | İşlenmiş sonuçlar | Verarbeitete Ergebnisse
├── scripts/        # Main Python code | Python kodları | Haupt-Python-Code
└── dist/           # Executable builds | Çalıştırılabilir dosyalar | Ausführbare Dateien

🔍 Sample Output Example / Örnek Çıktı / Beispielausgabe
product	sales	region
Laptop	999.9	Berlin
Mouse	29.9	Paris
⁉️ Support / Destek / Unterstützung

For help in your preferred language:

    📧 Email: kamil42konya@gmail.com

    💬 Discord: AutomatePro Community

<div align="center"> <sub>Developed with ❤️ by <a href="https://github.com/KamilCaliskan">Kamil Çalışkan</a></sub> | <sub>📅 Last Updated: 2025-08-01</sub> </div> 
