import cv2
import pytesseract
import os

# Tesseract path (Windows)
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_structured_data(image_path):
    if not os.path.exists(image_path):
        return {"Text": "Image file not found"}

    img = cv2.imread(image_path)
    if img is None:
        return {"Text": "Unable to read image"}

    # -------------------------
    # Preprocessing
    # -------------------------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # OCR
    raw_text = pytesseract.image_to_string(gray, config="--psm 6")

    print("🔍 OCR RAW TEXT:\n", raw_text)

    # Clean text
    cleaned_text = raw_text.strip()

    # -------------------------
    # 🚨 GUARANTEE EXCEL OUTPUT
    # -------------------------
    if not cleaned_text:
        return {"Text": "No readable text detected"}

    lines = [line.strip() for line in cleaned_text.splitlines() if line.strip()]

    data = {}

    # Case 1: Key-Value pairs
    if any(":" in line for line in lines):
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()

    # Case 2: Single word OR plain text
    else:
        for i, line in enumerate(lines, start=1):
            data[f"Text {i}"] = line

    return data

