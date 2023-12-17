#Weichzeichnen
'''
Beschreibung der Funktion:
Mit dieser Funktion kann ein Bild mit einer Unschärfe versehen werden.
In der Funktion selbst wird auf den linearen Filter "BloxBlur" zurückgegriffen.
Dieser setzt den Wert jedes Pixels auf den Dur
'''

#Import des Image Moduls der Bibliothek Pillow
from PIL import Image

#Import des ImageFilter Moduls der Bibliothek Pillow
from PIL import ImageFilter


import os

# Der Funktion werden ein Dateipfad zum Bild sowie der gewünschte Radius übergeben.
def weichzeichnen (image_path, radius):

    #Prüfung, ob der übergebene Radius dem Typ int oder float entspricht, wenn nicht, wird die Funktion beendet.
    if type(radius) == int or type(radius)== float:

        #Das Bild, mit dessen Dateipfad die Funktion geöffnet wurde, wird in die Variable "im" gespeichert.
        im = Image.open(image_path)

        #Anzeigen des importierten Bildes
        im.show()
        
        #Das durch den Blur Filter manipulierte Bild wird in der Variable "blured_img" gespeichert.
        blured_img = im.filter(ImageFilter.BoxBlur(radius))

        #Das manipulierte Bild wird angezeigt.
        blured_img.show()

        #In die Variable Dateiendung, wird die Dateiendung des in die Funktion importierten Bildes gespeichert.
        dateiendung = os.path.splitext(image_path)[1]

        #Bedingung prüft, welche Dateiendung in der Variablen "Dateiendung" gespeichert ist.
        #Bei ".jpg" wird das manipulierte Bild entsprechend als ".jpg" abgespeichert
        if (dateiendung == ".jpg"):
            blured_img.save("./images/blured_img.jpg")
            newimage_path= "./images/blured_img.jpg"
        
        #Bei ".png" wird das manipulierte Bild entsprechend als ".png" abgespeichert
        elif (dateiendung == ".png"):
            blured_img.save("./images/blured_img.png")
            newimage_path="./images/blured_img.png"

        #Gibt den Dateipfad des manipulierten Bildes aus    
        return newimage_path      
    else:
        print("Bitte wähle als Radius eine Zahl.")
    
unschaerfe_radius ("./images/cake.jpg", 10);