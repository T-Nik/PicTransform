
''' https://de.wikipedia.org/wiki/Invertieren_(Bildbearbeitung)#:~:text=In%20der%20Bildbearbeitung%20wird%20mit,aus%20schwarz%20wei%C3%9F%20und%20umgekehrt.'''

from PIL import Image
import numpy as np


def invert_image(image_path, output_path, preview=False):
    # Öffnen Sie das Bild mit Pillow
    img = Image.open(image_path)

    # Konvertieren Sie das Bild in ein Numpy-Array
    image_array = np.array(img)

    image_array = 255 - image_array

    # Erstellen Sie ein neues Bild mit den bearbeiteten Pixelwerten
    inverted_img = Image.fromarray(image_array)

    # Bild anzeigen lassen oder speichern
    if preview:
        print("Invertierung ausgelöst")
        inverted_img.show()
    else:
        # Speichern des Bildes
        print("Invertierung ausgelöst")
        inverted_img.save(image_path)

    return image_path + ""

    # Speichern Sie das bearbeitete Bild
    invert_img.save(output_path)
input_image_path = 'C:/Users/gille/Pictures/animal.jpeg'
output_image_path = 'C:/Users/gille/inverted_image.jpeg'

invert_image(input_image_path, output_image_path, preview=True)