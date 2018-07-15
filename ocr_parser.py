"""This file is the main point
of entry for OCR parsing
"""

# Built-in modules
import sys
import base64
import os
from PIL import Image

# Custom Modules
import parser
import pytesseract

# 3rd Party Modules
from wand.image import Image as WandImage
from wand.color import Color

def parse_image(image):
    """
    Takes in a Python Image object and returns all bank data
    Input Type: Python Image object
    Output Type: string that is csv compliant
    """
    contents = pytesseract.image_to_boxes(image)
    print(contents)
    structured = []
    # Pytesseract output is a big string so we have to break and parse out
    contents = contents.split('\n')
    for i in contents:
        data = i.split(' ') # More parsing out
        structured += [{
            'contents': data[0],
            'x': int(data[1]),
            'y': int(data[2])
        }]
    parsed = parser.parse_tesseract(structured)
    print(parsed)
    return parsed


if __name__ == '__main__':
    FILE_NAME = None
    try:
        FILE_NAME = sys.argv[1]
    except:
        print('Sorry buddy, but you need to provide a filename.')
        sys.exit()

    pil_pages = []
    if FILE_NAME[len(FILE_NAME)-4:len(FILE_NAME)] == '.pdf':
        with WandImage(filename=FILE_NAME, resolution=300) as pdf:
            for page_count, page in enumerate(pdf.sequence):
                page_image = WandImage(image=page)
                page_image.save(filename="reserved_name.png")
                pil_pages.append(Image.open("reserved_name.png"))
                print(pil_pages)
                os.remove("reserved_name.png")
    else:
        # Otherwise we assume it's an actual image file
        pil_pages = [Image.open(FILE_NAME)]
    
    for page in pil_pages: 
        parse_image(page)
    print('Done. Cheers!')
