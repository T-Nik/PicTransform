#Weichzeichnen
'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein Bild durch einen Weichzeichner mit einer Unschärfe versehen werden.
In der Funktion selbst wird auf den linearen Filter "BloxBlur" zurückgegriffen.

Vergleiche folgende Quellen anhand derer der Code implementiert wurde:
    Modul Image: https://pillow.readthedocs.io/en/stable/reference/Image.html
    Modul ImageFilter: https://pillow.readthedocs.io/en/stable/reference/ImageFilter.html
    Modul OS: https://docs.python.org/3/library/os.path.html
'''

#Import des Image-Moduls der Bibliothek Pillow
from PIL import Image

#Import des ImageFilter-Moduls der Bibliothek Pillow
from PIL import ImageFilter

#Import des OS-Moduls
import os

# Der Funktion werden ein Dateipfad zum Bild sowie der gewünschte Radius übergeben.
def weichzeichnen (image_path, radius):

    #Das Bild, mit dessen Dateipfad die Funktion geöffnet wurde, wird in die Variable "im" gespeichert.
    im = Image.open(image_path)

    #Anzeigen des importierten Bildes
    im.show()
        
    #Das durch den Blur Filter manipulierte Bild wird in der Variable "blured_img" gespeichert.
    blured_img = im.filter(ImageFilter.BoxBlur(radius))

    #Das manipulierte Bild wird angezeigt.
    blured_img.show()

    #In die Variable Dateiendung, wird die Dateiendung des in die Funktion importierten Bildes gespeichert.
    dateifpad, dateiendung = os.path.splitext(image_path)
    print (dateiendung)

    #Bedingung prüft, welche Dateiendung in der Variablen "Dateiendung" gespeichert ist.
    #Bei Dateiendung ".jpg" wird das manipulierte Bild entsprechend als ".jpg" abgespeichert
    if (dateiendung == ".jpg"):

        #Speichern des manipulierten Bildes im Ordner "Images" mit dem Dateinamen "Blured_img" und der Dateiendung ".jpg"
        blured_img.save("./images/blured_img.jpg")

        #Speichern des Dateipfades des manipulierten Bildes in die Variable "newimage_path"
        newimage_path= "./images/blured_img.jpg"
         
        #Bei Dateiendung ".png" wird das manipulierte Bild entsprechend als ".png" abgespeichert
    elif (dateiendung == ".png"):

        #Speichern des manipulierten Bildes im Ordner "Images" mit dem Dateinamen "Blured_img" und der Dateiendung ".png"
        blured_img.save("./images/blured_img.png")
            
        #Speichern des Dateipfades des manipulierten Bildes in die Variable "newimage_path"
        newimage_path="./images/blured_img.png"

    #Bei Dateiendung ".jpeg" wird das manipulierte Bild entsprechend als ".jpeg" abgespeichert
    elif (dateiendung == ".jpeg"):
           
        #Speichern des manipulierten Bildes im Ordner "Images" mit dem Dateinamen "Blured_img" und der Dateiendung ".jpeg"
        blured_img.save("./images/blured_img.jpeg")

       #Speichern des Dateipfades des manipulierten Bildes in die Variable "newimage_path"
        newimage_path= "./images/blured_img.jpeg"
    
    #Gibt den Dateipfad des manipulierten Bildes aus    
    return newimage_path      
    
#Testaufruf der Funktion
weichzeichnen ("./images/cake.jpg", 100);