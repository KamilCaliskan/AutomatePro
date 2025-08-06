from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from scripts.excel_automation import process_excel

# ====================== INITIALIZATION ======================
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

BASE_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = BASE_DIR / 'data' / 'input'
OUTPUT_FOLDER = BASE_DIR / 'data' / 'output'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ====================== HELPER FUNCTIONS ======================
def allowed_file(filename: str) -> bool:
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ====================== ROUTES ======================
@app.route('/process', methods=['POST'])
def process_file():
    """Handle file upload and processing"""
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if not allowed_file(file.filename):
        return jsonify(error="Only Excel files (.xlsx, .xls) allowed"), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = UPLOAD_FOLDER / filename
        file.save(input_path)

        # Process file
        output_filename = f"processed_{filename}"
        output_path = OUTPUT_FOLDER / output_filename

        success, message = process_excel(input_path, output_path)

        if success:
            return send_file(
                output_path,
                as_attachment=True,
                download_name=output_filename
            )
        else:
            return jsonify(error=message), 400

    except Exception as e:
        return jsonify(error=f"Processing error: {str(e)}"), 500

@app.route('/')
def index():
    return """
    <h1>Excel Processing Service</h1>
    <form method=post enctype=multipart/form-data action=/process>
      <input type=file name=file accept=".xlsx,.xls">
      <button type=submit>Process Excel</button>
    </form>
    """

# ====================== MAIN ======================
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5000)
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)
