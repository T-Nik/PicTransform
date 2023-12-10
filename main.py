#region Imports

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.config import Config

Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

# Imports für Image Import
import os
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView

# Ein Wait in der EventLoop damit sichergestellt ist das alle IDS initialisiert sind
from kivy.clock import Clock

#endregion Imports



#region Helpers

def copy_file(src, dst):
    # rb = read binary, wb = write binary
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            fdst.write(fsrc.read())

#endregion Helpers



#region GUI

class Controller(BoxLayout):
    pass

#endregion GUI




#region Main


class PicTransform(App):

    def build(self):
        root = Controller() # Root-Widget
        return root

    # Wird autom. aufgerufen nachdem das Fenster fertig gebaut wurde
    def on_start(self):
        print("IDs von root 'MainLayout': " + str(self.root.ids.keys())) # root ist das MainLayout
    
    # Funktion zum Öffnen des FileChoosers
    def open_fileChooser(self):
        # filter macht es möglich nur bestimmte Dateitypen zu wählen, alle anderne werden ausgeblendet
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        filechooser.bind(selection=self.selected) # bindet die Funktion select an die Auswahl des FileChoosers
        self.popup = Popup(title="Select an image", 
                        content=filechooser,
                        size_hint=(0.7, 0.7))
        self.popup.open()

    # Funktion zum Speichern des Bildes in images und Anzeigen des Bildes in ImageArea
    def selected(self, filechooser, selection):

        if selection:
            selected_path = selection[0]
            print("Gewähltes Bild: " + selected_path)

            # Kopieren des Bildes in den Ordner images
            destination_path = "images/" + os.path.basename(selected_path)
            copy_file(selected_path, destination_path)

            # Anzeigen des Bildes in ImageArea, durch anpassen des source-Attributs des image_widgets
            self.root.ids.image_widget.source = destination_path
            self.root.ids.image_widget.size_hint = (1, 1)

            self.popup.dismiss() # schließt das FileChooser-Popup


if __name__ == '__main__':
    PicTransform().run()

#endregion Main