"""Test_Reader runs a series of pytesseract methods on a sample file.
"""

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

FILE_NAME = "test_record.png"

# Simple image to string
print(pytesseract.image_to_string(Image.open(FILE_NAME)))

# French text image to string
print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

# Get bounding box estimates
print(pytesseract.image_to_boxes(Image.open(FILE_NAME)))

# Get verbose data including boxes, confidences, line and page numbers
print(pytesseract.image_to_data(Image.open(FILE_NAME)))

# Get informations about orientation and script detection
print(pytesseract.image_to_osd(Image.open(FILE_NAME)))
