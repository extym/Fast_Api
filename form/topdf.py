import pdfkit
from pdfkit import PDFKit

pdfkit.from_url('http://forma-avansa.tk:8000/form','out.pdf')

import weasyprint
from weasyprint.css.validation.properties import page



pdf = weasyprint.HTML('http://forma-avansa.tk:8000/form').write_pdf('goog.pdf',)

#open('google.pdf', 'wb').write(pdf)

# documents = weasyprint.HTML('http://forma-avansa.tk:8000/form2').render(optimize_size=0.8)
# all_pages = [p for doc in documents for p in doc.pages]
# documents[0].copy(all_pages).write_pdf('combined.pdf')

weasyprint.HTML('http://forma-avansa.tk:8000/form').write_pdf('weasyprint-website.pdf', zoom=1)
