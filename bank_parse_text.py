#!/usr/bin/python

import re
import sys
from xpdf_python import to_text

# hard-coding for BoA bank statements...
transactions_page_title = '***Page 3***'
trasnactions_section_title = 'TOTAL PAYMENTS AND OTHER CREDITS FOR THIS PERIOD'
transactions_section_end_title = 'TOTAL PURCHASES AND ADJUSTMENTS FOR THIS PERIOD'

state_regexp = re.compile(r'\b[A-Z]{2}\b$', re.MULTILINE)

def extract_text_from_pdf(pdf_location):
    """Extracts the text from a PDF at the specified location and writes it
      to a text file.

    Args:
      pdf_location (str): The location of the PDF to extract text from.

    Returns:
      (str, int): A tuple where the first element is the location of the
        text file containing the extracted text, and the second element is
        an int specifying the number of pages of text read from the PDF.
        If there was no text extracted from the PDF, this tuple will be ('', 0).
    """
    extracted_text, num_pages_extracted = to_text(pdf_location)

    if num_pages_extracted == 0:
      return ('', 0)

    extracted_text_location = pdf_location.split('.')[0] + '_extracted.txt'
    try:
      extracted_text_file = open(extracted_text_location, 'a')
      extracted_text_file.write(extracted_text)
      print('extracted', str(num_pages_extracted), 'pages of text to', extracted_text_location)
      return (extracted_text_location, num_pages_extracted)
    except:
      return ('', 0)

def parse_from_extracted_text_BoA(extracted_text_location):
  """Reads in extracted text from a Bank of America PDF statement and parses
  it into an array of transactions with metadata.

  Args:
    extracted_text_location (str): The location of the text file containing
      the extracted text.

  Returns:
    [{ 'date' : str, 'transaction' : str }]: An array of transactions (in
      dictionary format) that were successfuly parsed out of the text. Each
      transaction has an associated date and a string describing the name and
      location of the payee.
  """

  try:
    extracted_text_file = open(extracted_text_location)

    extracted_text = extracted_text_file.read()
    transactions_text = extracted_text.split(transactions_page_title)[1]

    payments_text = transactions_text.split(trasnactions_section_title)[1]
    payments_text = [line for line in payments_text.split('\n') if line.strip() != '']

    transaction_dates = payments_text[1].split(' ')
    # probably won't need posting dates, but here they are in case:
    #posting_dates = payments_text[2].split(' ')

    populated_transactions = []
    transaction_idx = 4
    dates_idx = 0
    while transaction_idx < len(payments_text):
      transaction = payments_text[transaction_idx]
      if transaction == transactions_section_end_title:
        break

      # dumb location parsing heuristic: if a line does not contain a state
      # code at the end, then we assume the next line is the location and group
      # the two together.
      if not state_regexp.search(transaction) and transaction_idx < len(payments_text) - 1:
        transaction = transaction + ' ' + payments_text[transaction_idx+1]
        transaction_idx += 1

      transaction_idx += 1
      populated_transactions.append({'date' : transaction_dates[dates_idx],
        'transaction' : transaction})
      dates_idx += 1
    return populated_transactions
  except:
    print('Error opening file', extracted_text_location)
    return []

def main():
  """Extracts the text from a (Bank of America) PDF file and parses it into
  an array of transactions with associated metadata.

  Usage:
    python3 parse_bank_text <PDF file name>
  """
  if len(sys.argv) != 2:
    print('Usage: python3 parse_bank_text.py <PDF file name>')

  pdf_location = sys.argv[1]

  txt_location, num_pages = extract_text_from_pdf(pdf_location)
  if num_pages == 0:
    print('Error: did not extract any text from pdf', pdf_location)
    exit(1)

  print(parse_from_extracted_text_BoA(txt_location))

if __name__ == "__main__":
    main()

