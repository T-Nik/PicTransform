#Unschärfe

from PIL import Image
from PIL import ImageFilter
from speichern import bildspeichern

im = Image.open("../images/cake.jpg")

def unschaerfe_radius (im, radius):
    if type(radius) == int or type(radius)== float:
        im.show()
        im2 = im.filter(ImageFilter.BoxBlur(radius))
        im2.show()
        #im2.save("upsi.jpg", None, quality=8)
        bildspeichern(im2)
    else:
        print("Bitte wähle als Radius eine Zahl.")
    
unschaerfe_radius (im, 10);