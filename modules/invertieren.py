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

    # Entscheidet, ob eine Vorschau des invertierten Bildes angezeigt oder das Bild gespeichert werden soll.
    if preview:
        # Wenn Vorschau gewünscht ist, gibt eine Meldung aus und zeigt die Vorschau an.
        print("Invertierung ausgelöst")
        inverted_img.show()
    else:
        # Wenn Vorschau nicht gewünscht ist, gibt eine Meldung aus und speichert das invertierte Bild.
        print("Invertierung ausgelöst")
        inverted_img.save(output_path)

    # Gibt den Dateipfad des invertierten Bildes zurück.
    return output_path

