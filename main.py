#region Imports

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

Config.set('graphics', 'width', '1366')
Config.set('graphics', 'height', '768')

# Imports für Image Import
import os
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView

# Aktionsleisten Widgets
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.label import Label


# Imports eigener Module
from modules.drehen import drehen

#endregion Imports



#region Helpers

def copy_file(src, dst):    
    # rb = read binary, wb = write binary
    try:
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                fdst.write(fsrc.read())
    except:
        print("Fehler beim Kopieren von " + src + " nach " + dst)
        return

#endregion Helpers



#region GUI

class Controller(BoxLayout):
    pass

#endregion GUI




#region Main


class PicTransform(App):
    actualImagePath = None

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
            self.actualImagePath = destination_path

            # Anzeigen des Bildes in ImageArea, durch anpassen des source-Attributs des image_widgets
            self.root.ids.image_widget.source = destination_path
            self.root.ids.image_widget.size_hint = (1, 1)

            self.popup.dismiss() # schließt das FileChooser-Popup


    # Funktion zum exportieren des Bildes
    def export_image(self):
        # Popup zum Auswählen des Speicherorts
        filechooser = FileChooserIconView(filters=['*'], dirselect=True)
        export_button = Button(text="Export", size_hint=(1, 0.1))
        export_button.bind(on_release=self.save_export)

        # Erstellen eines BoxLayouts für das Popup-Inhalt
        box_layout = BoxLayout(orientation='vertical')
        box_layout.add_widget(filechooser)
        box_layout.add_widget(export_button)

        self.export_popup = Popup(title="Select a save location", 
                                  content=box_layout,
                                  size_hint=(0.7, 0.7))
        self.export_popup.open()

    def save_export(self, instance):
        filechooser = self.export_popup.content.children[1]
        selection = filechooser.selection
        if selection:
            save_path = selection[0]
            copy_file(self.actualImagePath, os.path.join(save_path, os.path.basename(self.actualImagePath)))
            print(f"Bild exportiert nach: {save_path}")
            self.export_popup.dismiss()

    def clear_action_bar(self):
        # Entfernt alle Widgets aus der aktions_leiste
        self.root.ids.aktions_leiste.clear_widgets



    # "Drehen°"-Button
    def show_rotate_controls(self):
        self.clear_action_bar()

        # Altes label entfernen
        self.root.ids.aktions_leiste.remove_widget(self.root.ids.aktions_leiste_label)
        # Neues label hinzufügen für Grad°
        self.degree_label = Label(text='0°')
        self.root.ids.aktions_leiste.add_widget(self.degree_label)

        # Slider hinzufügen
        self.rotate_slider = Slider(min=0, max=360, value=0)
        self.rotate_slider.bind(value=lambda instance, value: setattr(self.degree_label, 'text', f'{int(value)}°'))
        self.root.ids.aktions_leiste.add_widget(self.rotate_slider)

        # Button hinzufügen
        self.apply_button = Button(text='Anwenden', on_release=self.apply_rotate)
        self.root.ids.aktions_leiste.add_widget(self.apply_button)

    def apply_rotate(self, callBackWidget):
        degrees = self.rotate_slider.value
        # Nachkommastellen enfternen
        degrees = int(degrees)

        # von ihr aus modules/drehen.py aufrufen
        print(drehen(self.actualImagePath, degrees))

        self.root.ids.image_widget.source = self.actualImagePath
        self.root.ids.image_widget.reload()


if __name__ == '__main__':
    PicTransform().run()

#endregion Main