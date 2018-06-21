try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

file_name = "test_record.png"

# Simple image to string
print(pytesseract.image_to_string(Image.open(file_name)))

# French text image to string
print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

# Get bounding box estimates
print(pytesseract.image_to_boxes(Image.open(file_name)))

# Get verbose data including boxes, confidences, line and page numbers
print(pytesseract.image_to_data(Image.open(file_name)))

# Get informations about orientation and script detection
print(pytesseract.image_to_osd(Image.open(file_name)))
