import pdfkit
from pdfkit import PDFKit

pdfkit.from_url('http://forma-avansa.tk:8000/form','out.pdf')


# def from_url(url, output_path, options=None, toc=None, cover=None,
#              configuration=None, cover_first=False):
#     """
#     Convert file of files from URLs to PDF document
#
#          : param url: url может быть URL или списком URL,
#          : param output_path: путь к выходному pdf, если установлено значение False, означает, что строка возвращается
#
#     Returns: True on success
#     """
#
#     r = PDFKit(url, 'url', options=options, toc=toc, cover=cover,
#                configuration=configuration, cover_first=cover_first)
#
#     return r.to_pdf(output_path)