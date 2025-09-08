from PyPDF2 import PdfReader, PdfWriter

reader = PdfReader("Bank 1.pdf")
writer = PdfWriter()


for page in reader.pages:
    page.compress_content_streams()  # This is CPU intensive!
    writer.add_page(page)

with open("smaller-new-file.pdf", "wb") as fp:
    writer.write(fp)