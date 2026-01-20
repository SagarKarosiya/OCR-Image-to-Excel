from flask import Flask, render_template, request, send_file
import os
import uuid

from utils.ocr_pipeline import extract_structured_data
from utils.excel_writer import save_to_excel

app = Flask(__name__)

# =========================
# FOLDERS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store last generated Excel file path
LAST_EXCEL_PATH = None


# =========================
# HOME + UPLOAD
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_EXCEL_PATH

    if request.method == "POST":

        # 1️⃣ Get uploaded image
        if "image" not in request.files:
            return "No file uploaded", 400

        image = request.files["image"]

        if image.filename == "":
            return "No selected file", 400

        # 2️⃣ Save image with unique name
        image_name = f"{uuid.uuid4()}_{image.filename}"
        image_path = os.path.join(UPLOAD_FOLDER, image_name)
        image.save(image_path)

        # 3️⃣ OCR extraction
        data = extract_structured_data(image_path)

        #if not data:                               """Disabled"""
        #    return render_template(
        #        "success.html",
        #        message="❌ OCR failed to detect text. Try a clearer image.",
        #        success=False
        #    )

        # 4️⃣ Create Excel
        excel_name = f"Extracted_Data_{uuid.uuid4().hex[:8]}.xlsx"
        excel_path = os.path.join(OUTPUT_FOLDER, excel_name)

        save_to_excel(data, excel_path)

        # ✅ FIXED LINE
        LAST_EXCEL_PATH = excel_path

        # 5️⃣ Success page
        return render_template(
            "success.html",
            message="✅ OCR completed successfully!",
            success=True
        )

    return render_template("index.html")


# =========================
# DOWNLOAD ROUTE
# =========================
@app.route("/download")
def download():
    global LAST_EXCEL_PATH

    if LAST_EXCEL_PATH is None or not os.path.exists(LAST_EXCEL_PATH):
        return "File not found. Please upload again.", 404

    return send_file(
        LAST_EXCEL_PATH,
        as_attachment=True,
        download_name="Extracted_Data.xlsx"
    )


# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app.run(debug=True)
