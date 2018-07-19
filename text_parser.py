import sys
import pdfquery

def extract_transactions(pdf):
    pages_in_pdf = len(pdf.pq('LTPage'))
    line_height = 9.84 # TODO: how to find this apart from hardcoding?
    transactions = []

    for page in range(1, pages_in_pdf + 1):
        purchases_header = pdf.pq(
            'LTPage[pageid=\'%s\'] \
            LTTextLineHorizontal:contains("Purchases and Adjustments")' % page)
        if purchases_header.attr('x0') is None or purchases_header.attr('y0') is None:
            continue
        print(purchases_header)
        x = float(purchases_header.attr('x0'))
        y = float(purchases_header.attr('y0'))

        t = pdf.extract([
            ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
            ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
             (x - 100, y - line_height, x + 500, y))
            ])['transactions']
        while len(t) == 6:
            t = ','.join([cell.text.strip() for cell in t])
            transactions.append(t)
            y -= line_height
            t = pdf.extract([
                ('with_parent', 'LTPage[pageid=\"%s\"]' % page),
                ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' %
                 (x - 100, y - line_height, x + 500, y))
                ])['transactions']
    return '\n'.join(transactions)

def text_parse(filename):
    # TODO: validate PDF file?
    pdf = pdfquery.PDFQuery(filename, normalize_spaces=False)
    pdf.load()
    return extract_transactions(pdf)

if __name__ == '__main__':
    filename = None
    try:
        filename = sys.argv[1]
    except:
        print('Sorry buddy, but you need to provide a filename.')
        sys.exit()

print(text_parse(filename))
