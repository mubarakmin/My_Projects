#Resizes an image and keeps aspect ratio. Set mywidth to the desired with in pixels.
import os
import PIL
from PIL import Image
import glob

mywidth = 2000 # Change the width

sdir = "" # Change Directory
all_images = glob.glob(sdir + "*.jpg")

for fname in all_images:
    
    sname = fname[0:-4] + "_resized.jpg"

    if os.path.exists(fname):
        img = Image.open(fname)
        wpercent = (mywidth/float(img.size[0]))
        #wpercent = 0.7
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
# If you need the images to rotate

        #img = img.transpose(Image.ROTATE_270)
        # if i == 1 or i == 2:
        #     img = img.transpose(Image.ROTATE_180)
		
        img.save(sname)
    else:
        print("File not found:", fname)
    print("processed %s" % fname)

print("done")