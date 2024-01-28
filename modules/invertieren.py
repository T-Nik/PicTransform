from PIL import Image
import numpy as np

# Die Funktion ermöglicht die Invertierung von Farben in einem Bild.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das invertiert werden soll.
# - output_path: Der Dateipfad für die Speicherung des invertierten Bildes.
# - preview: Gibt an, ob eine Vorschau des invertierten Bildes angezeigt werden soll (Standardwert ist False).
def invert_image(image_path, output_path, preview=False):
    try:
        # Parameter-Validierung
        if not isinstance(image_path, str) or not isinstance(output_path, str) or not isinstance(preview, bool):
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
            inverted_img.save(output_path)

        # Gibt den Dateipfad des invertierten Bildes zurück.
        return output_path

    except Exception as e:
        # Falls ein Fehler auftritt, gibt eine Fehlermeldung aus.
        print(f"Fehler bei der Invertierung des Bildes: {e}")


