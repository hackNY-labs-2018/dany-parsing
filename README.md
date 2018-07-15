# DANY Bank Parser

## Setup
*Before handover to DANY, we will have dockerized this code for easy deployment (I will check with Alex if this is a good idea.*
* Install virtualenv
* You should have a virtualenv created. This repository automatically ignores the `venv` folder so it would be a good name for a virtualenv. 
* Remember to activate your virtualenv with `source venv/bin/activate`
* Install all the dependencies with `pip install -r requirements.txt`. 
* Install imagemagick and libimagemagickdev (differs by platform). Available via apt on Ubuntu
* Install tesseract (see above.)

## Invoking
The main point of entry for this program is currently `ocr_parser.py`. To do OCR on a file, run: `python ocr_parser.py <FILE_NAME>`. If your file is a PDF, we will start by converting it to an image and then run OCR on it. If it is an image file, OCR will be run directly. We detect whether filetype entirely via extension. 
