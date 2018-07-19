import pdfquery

# pdf = pdfquery.PDFQuery("SAMPLE_CREDIT_CARD_STATEMENT.pdf")
pdf = pdfquery.PDFQuery("multipage_statement.pdf")
pdf.load()

pages_in_pdf = len(pdf.pq('LTPage'))

continued_str = "continued on next page..."

def extract_transactions():
  # TODO: are transactions always on the 3rd page?
  purchases_header = pdf.pq('LTPage[pageid="3"] LTTextLineHorizontal:contains("Purchases and Adjustments")')
  x = float(purchases_header.attr('x0'))
  y = float(purchases_header.attr('y0'))
  line_height = 9.84 # TODO: how to find this apart from hardcoding?
  transactions = []

  for page in range(1, pages_in_pdf + 1):
    t = pdf.extract([
        ('with_parent','LTPage[pageid=\"%s\"]' % page),
        ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
          y - line_height, x + 500, y))
        ])['transactions']
    while len(t) > 0:
      t = ','.join([cell.text.strip() for cell in t])
      transactions.append(t)
      y -= line_height
      t = pdf.extract([
        ('with_parent','LTPage[pageid=\"%s\"]' % page),
        ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
          y - line_height, x + 500, y))
        ])['transactions']

  # page_num = 3
  # t = pdf.extract([
  #     ('with_parent','LTPage[pageid=\"%s\"]' % page_num),
  #     ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
  #       y - line_height, x + 500, y))
  #     ])['transactions']
  # while len(t) > 0:
  #   t = ','.join([cell.text.strip() for cell in t])
  #   transactions.append(t)
  #   y -= line_height
  #   t = pdf.extract([
  #     ('with_parent','LTPage[pageid=\"%s\"]' % page_num),
  #     ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
  #       y - line_height, x + 500, y))
  #     ])['transactions']
  #   if len(t) == 0:
  #     page_num += 1
  #     t = pdf.extract([
  #       ('with_parent','LTPage[pageid=\"%s\"]' % page_num),
  #       ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
  #         y - line_height, x + 500, y))
  #       ])['transactions']

  # for i in range(50): # TODO temp..what if we have more?
  #   t = pdf.extract([
  #     ('with_parent','LTPage[pageid="3"]'),
  #     ('transactions', 'LTTextLineHorizontal:in_bbox("%s,%s,%s,%s")' % (x - 82,
  #       y - line_height, x + 500, y))
  #     ])['transactions']
  #   if len(t) == 0:
  #     break
  #   t = ','.join([cell.text.strip() for cell in t])
  #   transactions.append(t)
  #   y -= line_height

  return '\n'.join(transactions)

print(extract_transactions())