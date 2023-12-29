#Weichzeichnen
'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein Bild durch einen Weichzeichner mit einer Unschärfe versehen werden.
In der Funktion selbst wird auf den linearen Filter "BloxBlur" zurückgegriffen.

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    Modul ImageFilter: https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
    Modul OS: https://docs.python.org/3/library/os.path.html
'''

#Import des Image-Moduls der Bibliothek Pillow
from PIL import Image

#Import des ImageFilter-Moduls der Bibliothek Pillow
from PIL import ImageFilter

#Import des OS-Moduls
import os

# TODO: negativer Radius ermöglicht das bluren von bildern von -100 bis 0 und 0 bis 100 schärft das Bild

# Der Funktion werden ein Dateipfad zum Bild sowie der gewünschte Radius übergeben.
def weichzeichnen(image_path, radius, preview=True):

    #Das Bild, mit dessen Dateipfad die Funktion geöffnet wurde, wird in die Variable "im" gespeichert.
    im = Image.open(image_path)
    #Das durch den Blur Filter manipulierte Bild wird in der Variable "blured_img" gespeichert.
    blured_img = im.filter(ImageFilter.BoxBlur(radius))

    #Das manipulierte Bild wird angezeigt.
    if preview:
        blured_img.show()
        return "Weichzeichnen preview getriggered"
    else:
        blured_img.save(image_path)
        return image_path + " weichgezeichnet mit einem Radius von " + str(radius) + " Pixeln."