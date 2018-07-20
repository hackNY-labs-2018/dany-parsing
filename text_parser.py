"""Text Parser parses text directly from a PDF using the "pdfquery" library
"""

import os
import re
import sys

import pdfquery

def extract_transactions(pdf):
    """Extracts a list of all transactions in CSV format from a PDF
    """
    pages_in_pdf = len(pdf.pq('LTPage'))
    line_height = 9.84 # TODO: how to find this apart from hardcoding?
    transactions = []

    for page in range(1, pages_in_pdf + 1):
        purchases_header = pdf.pq(
            'LTPage[pageid=\'%s\'] \
            LTTextLineHorizontal:contains("Purchases and Adjustments")' % page)
        if purchases_header.attr('x0') is None or purchases_header.attr('y0') is None:
            continue
        x = float(purchases_header.attr('x0'))
        y = float(purchases_header.attr('y0'))

        t = pdf.extract([
            ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
            ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
             (x - 100, y - line_height, x + 500, y))
            ])['transactions']
        while len(t) == 6:
            t = ','.join([process_text_cell(cell) for cell in t])
            transactions.append(t)
            y -= line_height
            t = pdf.extract([
                ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
                ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
                 (x - 100, y - line_height, x + 500, y))
                ])['transactions']
    return '\n'.join(transactions)

def process_text_cell(cell):
    """Helper function to process each text cell extracted from a pdf
    """
    # regex that looks for multiple contiguous whitespace occurences (eg. multiple spaces)
    regex = r"\s\s+"
    # replaces regex matches with comma delineation, also strips whitespace from both ends
    return re.sub(regex, ",", cell.text.strip())

def text_parse(filename):
    """Parses text from a pdf
    """
    if not filename.endswith('.pdf'):
        print('Sorry, only PDF files are supported.')
        return ""
    # prevent space normalization in order to separate different text blocks in each line
    pdf = pdfquery.PDFQuery(
        filename,
        normalize_spaces=False,
        resort=False)
    pdf.load()
    return extract_transactions(pdf)

if __name__ == '__main__':
    # ensure filename is provided
    if len(sys.argv) != 2:
        print("Need exactly one argument for filename.")
        sys.exit()
    FILENAME = sys.argv[1]
    # execute
    OUTPUT = text_parse(FILENAME)
    print(OUTPUT)
    print('Writing to csv...')
    # write to csv
    OUTPUT_FILENAME = os.path.splitext(FILENAME)[0] + '.csv'
    with open(OUTPUT_FILENAME, 'w') as file:
        file.write(OUTPUT)
    print('Done, written to {0}'.format(OUTPUT_FILENAME))
