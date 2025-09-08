from PyPDF2 import PdfFileMerger

pdfs = ['1.pdf', '2.pdf']

merger = PdfFileMerger()

for pdf in pdfs:
    merger.append(pdf)

merger.write("complete.pdf")
merger.close()