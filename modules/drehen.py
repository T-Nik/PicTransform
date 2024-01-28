from PIL import Image

# Die Funktion "drehen" hat die Aufgabe, ein Bild um einen bestimmten Grad zu drehen.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das gedreht werden soll.
# - degrees: Der Rotationswinkel in Grad, um den das Bild gedreht werden soll.
# - preview: Gibt an, ob eine Vorschau des gedrehten Bildes angezeigt werden soll (Standardwert ist True).
def drehen(image_path, degrees, preview=True):
    
    try:
        # Öffnet das Bild mit Pillow und dreht es um den angegebenen Grad.
        img = Image.open(image_path)
        rotated_img = img.rotate(degrees, expand=False)
    except:
        # Gibt eine Fehlermeldung aus, wenn das Bild nicht geöffnet werden kann.
        print("Fehler beim Öffnen des Bildes")
        return

    # Falls das Bild um 90° oder 180° gedreht wird, behalten wir die Originaldimensionen bei.
    if degrees in [90, 180]:
        original_dimensions = img.size
        rotated_img = rotated_img.resize(original_dimensions, Image.Resampling.LANCZOS)  # Lanczos-Filter für bessere Qualität

    # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
    # oder das bearbeitete Bild wird gespeichert.
    if preview:
        print("Drehen preview getriggered")
        rotated_img.show()
    else:
        print("Drehen apply getriggered")
        rotated_img.save(image_path)

    # Gibt den Dateipfad des gedrehten Bildes zurück.
    return image_path + " gedreht um " + str(degrees) + " Grad°"
