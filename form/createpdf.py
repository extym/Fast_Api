import pdfkit
#import wkhtmltopdf

pdfkit.from_url('http://localhost:8000/form','out.pdf')