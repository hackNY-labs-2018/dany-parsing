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

def parse_images(images):
    """
    Takes in a list of Python Image objects and returns all bank data
    Input Type: list of Python Image objects
    Output Type: string that is csv compliant
    """
    contents = []
    count = 1
    for i in images:
        print('Running OCR on image {0}'.format(count))
        content = pytesseract.image_to_boxes(i)
        content = content.split('\n')
        structured = []
        # Pytesseract output is a big string so we have to break and parse out
        for i in content:
            data = i.split(' ') # More parsing out
            structured += [{
                'contents': data[0],
                'x': int(data[1]),
                'y': int(data[2])
            }]
        contents += [structured]
        count += 1
    parsed = parser.parse_tesseract(contents)
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
                os.remove("reserved_name.png")
    else:
        # Otherwise we assume it's an actual image file
        pil_pages = [Image.open(FILE_NAME)]
    
    csv_data = parse_images(pil_pages)
    print(csv_data)
    print('Done. Cheers!')
