import pandas as pd
import os

def save_to_excel(data, excel_path):
    """
    Save extracted OCR data into an Excel file
    """

    if not data:
        raise ValueError("No data to save")

    df = pd.DataFrame(list(data.items()), columns=["Field", "Value"])

    os.makedirs(os.path.dirname(excel_path), exist_ok=True)

    df.to_excel(excel_path, index=False)

    print(f"✅ Excel saved at: {excel_path}")
