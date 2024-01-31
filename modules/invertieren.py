# Bild invertieren

'''
Beschreibung der Funktion:
Mit dieser Funktion können die Farben in einem importierten Bild invertiert werden.
Parameter:
    - image_path: Der Dateipfad zum Bild, dessen Farben invertiert werden sollen (String).
    - preview: Gibt an, ob eine Vorschau des invertierten Bildes angezeigt werden soll (Standardwert ist False).

Die Parameter-Validierung wurde mit Unterstützung von ChatGPT implementiert.
'''

from PIL import Image
import numpy as np
from modules.fehler_popup import show_error_popup

def invert_image(image_path, preview=False):
    try:
        # Parameter-Validierung (Unterstützung von ChatGPT)
        if not isinstance(image_path, str) or not isinstance(preview, bool):
            raise TypeError("Ungültige Parameter. 'image_path' und 'output_path' müssen Zeichenketten (Strings) sein, 'preview' muss ein boolescher Wert sein.")

        # Öffnen Sie das Bild mit Pillow.
        img = Image.open(image_path)

        # Konvertieren Sie das Bild in ein Numpy-Array.
        image_array = np.array(img)

        # Invertiert die Farben im Bild durch Subtraktion von jedem Pixelwert von 255.
        image_array = 255 - image_array

        # Erstellen Sie ein neues Bild mit den bearbeiteten Pixelwerten.
        inverted_img = Image.fromarray(image_array)

        # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
        # oder das bearbeitete Bild wird gespeichert.
        if preview:
            print("Invertierung Preview ausgelöst")
            inverted_img.show()
        else:
            print("Invertierung apply ausgelöst")
            inverted_img.save(image_path)

        # Gibt den Dateipfad des invertierten Bildes zurück.
        return image_path + " invertiert."

    except Exception as e:
        # Falls ein Fehler auftritt, gibt eine Fehlermeldung aus.
        show_error_popup(f"Fehler bei der Invertierung des Bildes: {e}")