import utils
from utils.ocr_pipeline import extract_structured_data


result = extract_structured_data("sample.png")
print(result)
