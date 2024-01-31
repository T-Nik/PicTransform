# Bild drehen

'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein importiertes Bild um einen bestimmten Grad gedreht werden.
Parameter:
    - image_path: Der Dateipfad zum Bild, das gedreht werden soll (String).
    - degrees: Der Rotationswinkel in Grad, um den das Bild gedreht werden soll.
    - preview: Gibt an, ob eine Vorschau des gedrehten Bildes angezeigt werden soll (Standardwert ist True).

Die Parameter-Validierung wurde mit Unterstützung von ChatGPT implementiert.
'''

from PIL import Image
from modules.fehler_popup import show_error_popup

def drehen(image_path, degrees, preview=True):
    
    try:
        # Parameter-Validierung (Unterstützung von ChatGPT)
        if not isinstance(image_path, str):
            raise TypeError("Ungültiger Parameter. 'image_path' muss ein String sein.")
        if not isinstance(degrees, (int, float)):
            raise TypeError("Ungültiger Parameter. 'degrees' muss eine Zahl sein.")
        if not isinstance(preview, bool):
            raise TypeError("Ungültiger Parameter. 'preview' muss ein Boolean-Wert sein.")
        
        # Öffnet das Bild mit Pillow und dreht es um den angegebenen Grad.
        img = Image.open(image_path)
        rotated_img = img.rotate(degrees, expand=False)
    

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
    
    except TypeError as e:
        # Gibt eine Fehlermeldung aus, wenn das Bild nicht geöffnet werden kann.
        show_error_popup(f"Fehler bei der Parameter-Validierung: {e}")