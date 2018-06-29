from xpdf_python import to_text

pdf_location = 'DO_NOT_COMMIT_ME_THIS_HAS_IMPORTANT_INFO/bank_statement.pdf'
text = to_text(pdf_location)

print(text)
