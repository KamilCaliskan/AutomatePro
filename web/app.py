from werkzeug.utils import secure_filename
from flask import Flask, request, send_file
import os
from pathlib import Path
import traceback

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

# Input and output folders
UPLOAD_FOLDER = BASE_DIR / 'data' / 'input'
OUTPUT_FOLDER = BASE_DIR / 'data' / 'output'

# Allowed Excel extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

# Ensure upload and output directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process', methods=['POST'])
def process():
    print("\n=== NEW REQUEST ===")  # Debug log
    try:
        if 'file' not in request.files:
            print("❌ No file part in request")  # Debug
            return "No file part", 400

        file = request.files['file']
        print(f"📦 Received file: {file.filename}")  # Debug

        if file.filename == '':
            print("❌ Empty filename")  # Debug
            return "No selected file", 400

        if not allowed_file(file.filename):
            print(f"❌ Invalid file type: {file.filename}")  # Debug
            return "Invalid file type. Only .xlsx and .xls are allowed.", 400

        # Secure and save uploaded file
        filename = secure_filename(file.filename)
        input_path = UPLOAD_FOLDER / filename
        print(f"💾 Saving to: {input_path}")  # Debug

        file.save(input_path)
        print(f"✅ File saved successfully")  # Debug

        # Define output path
        output_path = OUTPUT_FOLDER / f'processed_{filename}'
        os.makedirs(output_path.parent, exist_ok=True)
        print(f"📂 Output will go to: {output_path}")  # Debug

        # Import and call the processing function
        from scripts.excel_automation import process_excel
        success = process_excel(input_path, output_path)
        print(f"⚙️ Processing result: {success}")  # Debug

        if success:
            print("✅ Sending processed file back to client")
            return send_file(output_path, as_attachment=True)

        print("❌ Processing failed inside process_excel")
        return "Processing failed", 500

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}", flush=True)
        traceback.print_exc()
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Run Flask app on all interfaces, port 5000, debug mode enabled
    app.run(host='0.0.0.0', port=5000, debug=True)
