import os
from PIL import Image
from fpdf import FPDF
import glob
pdf = FPDF()
sdir = "" # Your directory
w,h = 0,0

all_images = glob.glob(sdir + "*.jpg")

#for i in range(1, 31):
for fname in all_images:
    if os.path.exists(fname):
        if fname == all_images[0]:
            cover = Image.open(fname)
            # cover = cover.transpose(Image.ROTATE_90)
            w,h = cover.size
            pdf = FPDF( unit = "pt", format = [w,h])
        image = fname
        pdf.add_page()
        pdf.image(image,0,0,w,h)
    else:
        print("File not found:", fname)
    print("processed %s" % fname)
pdf.output("complete.pdf", "F")
print("done")