#Auflösung anpassen

'''
Beschreibung der Funktion:
Mit dieser Funktion kann die Auflösung eines importierten Bildes angepasst werden.

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    
'''
    
#Import des Image-Moduls der Bibliothek Pillow
from PIL import Image

#Import des ImageFilter-Moduls der Bibliothek Pillow
from PIL import ImageFilter

# Der Funktion werden ein Dateipfad zum Bild sowie die gewünschte neue Auflösung (bestehtend aus Höhe und Breite) übergeben.
def aufloesung (image_path, breite, hoehe, preview=True):
    try:
        im = Image.open(image_path)
        resized_img = im.resize([hoehe, breite])
        
        #Das manipulierte Bild wird angezeigt.
        if preview:
            resized_img.show()
            return "Aufloesung preview getriggered"
        else:
            resized_img.save(image_path)
            return image_path + " Auflösung geändert auf Breite:" + str(breite) + " und Höhe: " + str(hoehe) + "."

    except ValueError:
            print("Es ist ein Fehler aufgetreten. Die Werte müssen über 0 liegen.")

#aufloesung(r"G:\Downloads\test.jpg",600,9000, True)