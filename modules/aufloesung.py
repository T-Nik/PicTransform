# Auflösung anpassen

'''
Beschreibung der Funktion:
Mit dieser Funktion kann die Auflösung eines importierten Bildes angepasst werden.

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    
'''
    
# Import des Image-Moduls der Bibliothek Pillow
from PIL import Image


# Die Funktion "aufloesung" ändert die Auflösung eines importierten Bildes.
# Parameter:
# - image_path: Der Dateipfad zum Bild, dessen Auflösung geändert werden soll.
# - breite: Die neue Breite des Bildes.
# - hoehe: Die neue Höhe des Bildes.
# - preview: Gibt an, ob eine Vorschau des veränderten Bildes angezeigt werden soll (Standardwert ist True).
def aufloesung(image_path, breite, hoehe, preview=True):
    try:
        # Parameter-Validierung
        if not isinstance(image_path, str):
            raise TypeError("Ungültiger Parameter. 'image_path' muss ein String sein.")
        if not isinstance(breite, int) or breite <= 0:
            raise ValueError("Ungültiger Parameter. 'breite' muss eine positive ganze Zahl sein.")
        if not isinstance(hoehe, int) or hoehe <= 0:
            raise ValueError("Ungültiger Parameter. 'hoehe' muss eine positive ganze Zahl sein.")
        if not isinstance(preview, bool):
            raise TypeError("Ungültiger Parameter. 'preview' muss ein Boolean-Wert sein.")

        # Öffnet das Bild mit Pillow und ändert seine Auflösung.
        im = Image.open(image_path)
        resized_img = im.resize([hoehe, breite])
        
        # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
        # oder das bearbeitete Bild wird gespeichert.
        if preview:
            resized_img.show()
            return "Aufloesung preview getriggered"
        else:
            resized_img.save(image_path)
            return image_path + " Auflösung geändert auf Breite:" + str(breite) + " und Höhe: " + str(hoehe) + "."

    except ValueError as ve:
        # Gibt eine Fehlermeldung aus, wenn ungültige Werte für Breite oder Höhe angegeben werden.
        print(f"Es ist ein Fehler aufgetreten: {ve}")
