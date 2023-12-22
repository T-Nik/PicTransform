# Autor: <your name>
'''
    Beschreibung:  Die Funktion "drehen" in dem gegebenen code hat die Aufgabe, ein Bild zu öffnen, es um einen bestimmten Grad zu drehen, und je nach Rotationswinkel das Bild in die Originaldimensionen zu ändern, um die ursprüngliche Auflösung beizubehalten.
'''

from PIL import Image

def drehen(image_path, degrees, preview=True):
    
    try:
        img = Image.open(image_path)
        rotated_img = img.rotate(degrees, expand=False)
    except:
        print("Fehler beim Öffnen des Bildes")
        return

    # Falls das Bild um 90° oder 180° gedreht wird, behalten wir die Originaldimensionen bei
    if degrees in [90, 180]:
        original_dimensions = img.size
        rotated_img = rotated_img.resize(original_dimensions, Image.Resampling.LANCZOS) # Lanczos-Filter für bessere Qualität

    # Bild anzeigen lassen
    if preview:
        print("Drehen preview getriggered")
        rotated_img.show()
    else:
        # Speichern des Bildes
        print("Drehen apply getriggered")
        rotated_img.save(image_path)

    return image_path + " gedreht um " + str(degrees) + " Grad°"
