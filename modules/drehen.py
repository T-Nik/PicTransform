# Autor: <your name>
'''
    Beschreibung:
'''

from PIL import Image


# Sry musste es schonmal testen :D
# TODO: Wenn das Bild nicht um 90° oder 180° gedreht wird, verändert sich die Auflösung, da könntest du nochmal schauen, ob es dafür einen fix gibt mit img.show() kannst du dir das Bild vorher ausgeben lassen
def drehen(image_path, degrees):
    
    img = Image.open(image_path)
    if degrees == 90 or degrees == 180:
        rotated_img = img.rotate(degrees, expand=True) # expand=True verhindert das Abschneiden des Bildes und verändert die Größe des Bildes
    else:
        rotated_img = img.rotate(degrees)
    
    original_dimensions = img.size
    resized_img = rotated_img.resize(original_dimensions, Image.ANTIALIAS)

    # Bild anzeigen lassen
    rotated_img.show()

    # Speichern des Bildes
    rotated_img.save(image_path)

    return image_path + " gedreht um " + str(degrees) + " Grad°"
