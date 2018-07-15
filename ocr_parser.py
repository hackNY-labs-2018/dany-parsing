"""This file is the main point
of entry for OCR parsing
"""

# Built-in modules
import sys
import base64
from PIL import Image

# Custom Modules
import parser

# 3rd Party Modules
from wand.image import Image as WandImage


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
    import pytesseract

    FILE_NAME = None
    try:
        FILE_NAME = sys.argv[1]
    except:
        print('Sorry buddy, but you need to provide a filename.')
        sys.exit()

    image = None
    if FILE_NAME[len(FILE_NAME)-4:len(FILE_NAME)] == '.pdf':
        with WandImage(filename=FILE_NAME, resolution=300) as pdf:
            page_index = 0
            height = pdf.height
            with WandImage(width=pdf.width,
                height=len(pdf.sequence)*height) as png:
                for page in pdf.sequence:
                    png.composite(page, 0, page_index * height)
                    page_index += 1
                png.save(filename="xxx.png")
                image = Image.open("xxx.png")
            
    else:
        # Otherwise we assume it's an actual image file
        image = Image.open(FILE_NAME)
    parse_image(image)
    print('Done. Cheers!')
