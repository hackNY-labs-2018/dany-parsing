##############################
# This file is the main point
# of entry for OCR parsing
##############################

# Built-in modules
import sys
import base64

# 3rd Party Modules
from wand.image import Image as WandImage

# Custom Modules
import parser

def parse_image(image):
    """
    Takes in a Python Image object and returns all bank data
    Input Type: Python Image object
    Output Type: string that is csv compliant
    """
    contents = pytesseract.image_to_boxes(image)
    print(contents)
    structured = []
    contents = contents.split('\n') # Pytesseract output is a big string so we have to break and parse out
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
    try:
        import Image
    except ImportError:
        from PIL import Image
    import pytesseract

    file_name = None
    try:
        file_name = sys.argv[1]
    except:
        print('Sorry buddy, but you need to provide a filename.')
        sys.exit()

    image = None
    if file_name[len(file_name)-4:len(file_name)] == '.pdf':
        with WandImage(filename=file_name, resolution=300) as img:
            with WandImage(blob=base64.b64decode(img), width=img.width, height=img.height, format='png') as bg:
                bg.composite(img, 0, 0)
                image = bg
    else:
        # Otherwise we assume it's an actual image file
        image = Image.open(file_name)
    parse_image(image)
    print('Done. Cheers!')
