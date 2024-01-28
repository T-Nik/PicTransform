from PIL import Image
import numpy as np

# Die Funktion ermöglicht die Invertierung von Farben in einem Bild.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das invertiert werden soll.
# - output_path: Der Dateipfad für die Speicherung des invertierten Bildes.
# - preview: Gibt an, ob eine Vorschau des invertierten Bildes angezeigt werden soll (Standardwert ist False).
def invert_image(image_path, output_path, preview=False):
    # Öffnen Sie das Bild mit Pillow.
    img = Image.open(image_path)

    # Konvertieren Sie das Bild in ein Numpy-Array.
    image_array = np.array(img)

    # Invertiert die Farben im Bild durch Subtraktion von jedem Pixelwert von 255.
    image_array = 255 - image_array

    # Erstellen Sie ein neues Bild mit den bearbeiteten Pixelwerten.
    inverted_img = Image.fromarray(image_array)

    # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
    # oder das bearbeitete Bild wird gespeichert, und eine Erfolgsmeldung mit dem Pfad und dem Radius wird zurückgegeben.
    if preview:
        print("Invertierung ausgelöst")
        inverted_img.show()
    else:
        print("Invertierung ausgelöst")
        inverted_img.save(output_path)

    # Gibt den Dateipfad des invertierten Bildes zurück.
    return output_path

