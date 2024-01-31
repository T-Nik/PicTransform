# Weichzeichnen oder Schärfen

'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein importiertes Bild durch eine Unscharfmaskierung geschärft oder
durch Weichzeichnungseffekte weichgezeichnet werden.
Parameter:
    - image_path: Der Dateipfad zum Bild, auf dem der Weichzeichnungseffekt oder die
      Unscharfmaskierung angewendet werden soll (String).
    - radius: Der Radius für den Weichzeichnungseffekt oder die Unscharfmaskierung (int oder float).
    - preview: Gibt an, ob eine Vorschau des bearbeiteten Bildes angezeigt werden soll (Standardwert ist True).

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    Modul ImageFilter: https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html

Die Parameter-Validierung wurde mit Unterstützung von ChatGPT implementiert. 
'''

# Import des Image-Moduls der Bibliothek Pillow
from PIL import Image

# Import des ImageFilter-Moduls der Bibliothek Pillow
from PIL import ImageFilter

from modules.fehler_popup import show_error_popup

def weichzeichnen(image_path, radius, preview=True):
    try:
        # Parameter-Validierung (Unterstützung von ChatGPT)
        if not isinstance(image_path, str):
            raise TypeError("Der Dateipfad zum Bild muss eine Zeichenkette (String) sein.")
            
        if not isinstance(radius, (int, float)):
            raise TypeError("Der Radius muss eine Zahl sein.")
            
        if not isinstance(preview, bool):
            raise TypeError("Der Vorschau-Parameter muss ein boolscher Wert sein.")
    
    
        # Das Bild, mit dessen Dateipfad die Funktion aufgerufen wurde, wird in die Variable "im" gespeichert.
        im = Image.open(image_path)

        # Prüfung, ob das Bild mit einer Unschärfe versehen oder geschärft werden soll.
        if radius < 0 and radius > -100:
            # Die Funktion BoxBlur kann nur mit positiven Zahlen arbeiten, daher wird der Radius in eine positive Zahl gewandelt.
            radius = radius * -1

            # Das Bild wird mit dem eingegebenen Radius weichgezeichnet.
            # Jedes Pixel im Bild wird durch einen gewichteten Durchschnitt seiner Nachbarpixel ersetzt. 
            # Der Parameter radius in ImageFilter.BoxBlur(radius) gibt an, wie weit der Weichzeichnungseffekt in das Bild hineinreichen soll.
            blured_img = im.filter(ImageFilter.BoxBlur(radius))           

        # Zweite Prüfung, bei einem Radius zwischen 0 und 100 soll das Bild geschärft werden.
        elif radius > 0 and radius < 100:
            # Das Bild wird mit dem eingegebenen Radius geschärft.
            # Die Unscharfmaskierung wirkt, indem sie einen gewichteten Unterschied zwischen den Pixeln und ihren benachbarten Pixeln berechnet und diesen auf das Originalbild addiert. 
            # Dieser Prozess hebt die Kanten im Bild hervor und erzeugt den Eindruck von Schärfe.
            blured_img = im.filter(ImageFilter.UnsharpMask(radius))

        # Fängt mögliche Eingaben für einen Radius ab, mit denen die Funktion nicht umgehen kann.
        else:
            print("Der Radius muss zwischen -100 und +100 liegen und darf nicht 0 sein.")
            return

        # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
        # oder das bearbeitete Bild wird gespeichert, und eine Erfolgsmeldung mit dem Pfad und dem Radius wird zurückgegeben.
        if preview:
            blured_img.show()
            return "Weichzeichnen-Vorschau ausgelöst"
        else:
            blured_img.save(image_path)
            return image_path + " weichgezeichnet mit einem Radius von " + str(radius) + " Pixeln."
        
    except TypeError as e:
        show_error_popup(f"Fehler bei der Parameter-Validierung: {e}")

    except Exception as e:
        # Fängt allgemeine Ausnahmen ab und gibt eine Fehlermeldung aus.
        print(f"Es ist ein Fehler aufgetreten: {e}")
