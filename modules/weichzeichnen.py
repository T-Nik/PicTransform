#Weichzeichnen oder Schärfen
'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein Bild durch einen Weichzeichner mit einer Unschärfe versehen werden oder geschärft werden.
In der Weichzeichnenfunktion wird auf den linearen Filter "BloxBlur" und in der Schärfenfunktion auf die Funktion "UnsharpMask" zurückgegriffen.

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    Modul ImageFilter: https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
'''

#Import des Image-Moduls der Bibliothek Pillow
from PIL import Image

#Import des ImageFilter-Moduls der Bibliothek Pillow
from PIL import ImageFilter

# Der Funktion werden ein Dateipfad zum Bild sowie der gewünschte Radius übergeben.
def weichzeichnen(image_path, radius, preview=True):
    try:
        #Das Bild, mit dessen Dateipfad die Funktion aufgerufen wurde, wird in die Variable "im" gespeichert.
        im = Image.open(image_path)

        #Prüfung, ob das Bild mit einer Unschärfe versehen werden soll oder geschärft werden soll.        
        if radius < 0 and radius > -100:
            #Die Funktion BoxBlur kann nur mit positiven Zahlen arbeiten, daher wird der Radius in eine positive Zahl gewandelt.
            radius = radius*-1

            #Das Bild wird mit dem eingegebenen Radius weichgezeichnet
            blured_img = im.filter(ImageFilter.BoxBlur(radius))           

        #zweite Prüfung, bei einem Radius zwischen 0 und 100 soll das Bild geschärft werden.
        elif radius > 0 and radius <100:
            #Das Bild wird mit dem eingegebenen Radius geschärft
            blured_img = im.filter(ImageFilter.UnsharpMask(radius))

        #fängt mögliche Eingaben für einen Radius ab, mit denen die Funktion nicht umgehen kann
        else:
            print("Der Radius muss zwischen -100 und +100 liegen und darf nicht 0 sein.")
            return

            #Das manipulierte Bild wird angezeigt.
        if preview:
            blured_img.show()
            return "Weichzeichnen preview getriggered"
        else:
            blured_img.save(image_path)
            return image_path + " weichgezeichnet mit einem Radius von " + str(radius) + " Pixeln."
         
    except:
        print("Es ist ein Fehler aufgetreten.")
