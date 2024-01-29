#region Imports

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config

# Start Auflösung der App, nach Start Responsive skalierbar
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
from kivy.uix.dropdown import DropDown
from kivy.uix.scrollview import ScrollView


# Imports eigener Module
# Drehenfunktion in Grad
from modules.drehen import drehen

# Weichzeichnen- und Schärfenfunktion
from modules.weichzeichnen import weichzeichnen

# Filterfunktionen 
import modules.filter as filter
from modules.filter import Filter_Presets

# Objekterkennungsfunktionen
from modules.objectDetection import object_detection

# Metadatenfunktion
from modules.meta_data.ImageMetaData_Module import ImageMetaData

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

    # Funktion zum Exportieren des Bildes
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
        try:
            if self.actualImagePath is None:
                raise ValueError("Es wurde kein Bild importiert.")

            filechooser = self.export_popup.content.children[1]
            selection = filechooser.selection
            if selection:
                save_path = selection[0]
                copy_file(self.actualImagePath, os.path.join(save_path, os.path.basename(self.actualImagePath)))
                print(f"Bild exportiert nach: {save_path}")
                self.export_popup.dismiss()

        except ValueError as e:
            print(f"Fehler beim Exportieren des Bildes: {e}")

    def clear_action_bar(self):
        # Entfernt alle Widgets aus der aktions_leiste
        self.root.ids.aktions_leiste.clear_widgets()


#region "Filter"
    def show_filter_controls(self):
        self.clear_action_bar()

        # Label für Dropdown-Menü hinzufügen
        self.filter_label = Label(text='Filter:')

        # Dropdown-Menü erstellen
        self.filter_dropdown = DropDown()
        self.drop_down_button = Button(text=str(Filter_Presets.current_filter), height=50, size_hint_y=None, color=(0, 0, 0, 1))

        # Dropdown-Menü mit filter_label in ein vertikales Box_Layout
        self.filter_box_layout = BoxLayout(orientation='vertical', size_hint_x=None, width=200)
        self.filter_box_layout.add_widget(self.filter_label)
        self.filter_box_layout.add_widget(self.drop_down_button)
        self.root.ids.aktions_leiste.add_widget(self.filter_box_layout)

        for filter_name in Filter_Presets.filter_dict.keys():
            btn = Button(text=filter_name, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.filter_dropdown.select(btn.text))
            self.filter_dropdown.add_widget(btn)

        # Dropdown öffnen, wenn der Button gedrückt wird
        self.drop_down_button.bind(on_release=self.filter_dropdown.open)
        # Aktualisieren des Textes des Buttons, wenn ein Eintrag im Dropdown ausgewählt wird
        self.filter_dropdown.bind(on_select=lambda instance, x: setattr(self.drop_down_button, 'text', x))

        # Button hinzufügen
        self.preview_button = Button(text='Vorschau', on_release=self.preview_filter, background_color=(1, 1, 1, 0.5))
        self.root.ids.aktions_leiste.add_widget(self.preview_button)
        self.apply_button = Button(text='Anwenden', on_release=self.apply_filter, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)


    def preview_filter(self, callBackWidget):
        Filter_Presets.filter_dict[self.drop_down_button.text].apply_config(self.actualImagePath, preview=True)

    def apply_filter(self, callBackWidget):
        Filter_Presets.filter_dict[self.drop_down_button.text].apply_config(self.actualImagePath, preview=False)
        self.root.ids.image_widget.source = self.actualImagePath
        self.root.ids.image_widget.reload()
#endregion "Filter"


#region "Drehen°"
    def show_rotate_controls(self):
        self.clear_action_bar()

        # Neues label hinzufügen für Grad°
        self.degree_label = Label(text='0°')
        self.root.ids.aktions_leiste.add_widget(self.degree_label)

        # Slider hinzufügen
        self.rotate_slider = Slider(min=0, max=360, value=0)
        self.rotate_slider.bind(value=lambda instance, value: setattr(self.degree_label, 'text', f'{int(value)}°'))
        self.root.ids.aktions_leiste.add_widget(self.rotate_slider)

        # "Vorschau" Button hinzufügen
        self.preview_button = Button(text='Vorschau', on_release=self.preview_rotate, background_color=(1, 1, 1, 0.5))
        self.root.ids.aktions_leiste.add_widget(self.preview_button)

        # "Anwenden" Button hinzufügen
        self.apply_button = Button(text='Anwenden', on_release=self.apply_rotate, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)
        

    def preview_rotate(self, callBackWidget):
        degrees = self.rotate_slider.value
        # Nachkommastellen enfternen
        degrees = int(degrees)
        # von ihr aus modules/drehen.py aufrufen
        print(drehen(self.actualImagePath, degrees, preview=True))

    def apply_rotate(self, callBackWidget):
        degrees = self.rotate_slider.value
        # Nachkommastellen enfternen
        degrees = int(degrees)
        # von ihr aus modules/drehen.py aufrufen
        print(drehen(self.actualImagePath, degrees, preview=False))
        self.root.ids.image_widget.source = self.actualImagePath
        self.root.ids.image_widget.reload()
#endregion "Drehen°"


#region "Weichzeichnen"
    def show_blur_controls(self):
        self.clear_action_bar()
        
        # Neues label hinzufügen für Stärke
        self.degree_label = Label(text='0%')
        self.root.ids.aktions_leiste.add_widget(self.degree_label)

        # Slider hinzufügen
        self.blur_slider = Slider(min=0, max=100, value=0)
        self.blur_slider.bind(value=lambda instance, value: setattr(self.degree_label, 'text', f'{int(value)}%'))
        self.root.ids.aktions_leiste.add_widget(self.blur_slider)

        # "Vorschau" Button hinzufügen
        self.preview_button = Button(text='Vorschau', on_release=self.preview_blur, background_color=(1, 1, 1, 0.5))
        self.root.ids.aktions_leiste.add_widget(self.preview_button)

        # "Anwenden" Button hinzufügen
        self.apply_button = Button(text='Anwenden', on_release=self.apply_blur, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)
        

    def preview_blur(self, callBackWidget):
        radius = self.blur_slider.value
        # Nachkommastellen enfternen
        radius = int(radius)
        print(weichzeichnen(self.actualImagePath, radius, preview=True))

    def apply_blur(self, callBackWidget):
        radius = self.blur_slider.value
        # Nachkommastellen enfternen
        radius = int(radius)
        print(weichzeichnen(self.actualImagePath, radius, preview=False))
        self.root.ids.image_widget.source = self.actualImagePath
        self.root.ids.image_widget.reload()
#endregion "Weichzeichnen"
        

#region "Objekt Erkennung"
    def show_objectDetection_controls(self):
        self.clear_action_bar()

        # Klassenlabels laden
        with open("nn_model/coco.names", "r") as f:
            LABELS = f.read().strip().split("\n")
        
        # Neues label hinzufügen für Stärke
        self.label = Label(
            text=f'Objekt Erkennung mit YOLOv3-tiny (COCO) zur Klassifizierung von 80 Objekten:\n\n {LABELS} \n\nDieses Modell ist ein Convolutional NN mit genau 8.849.182 Parametern',
            size_hint_y=None,  # Erlaubt dem Label, seine Höhe basierend auf dem Inhalt anzupassen
            text_size=(350, None),  # Setzt die Breite für den Textumbruch, Höhe ist unbegrenzt
            halign='left',  # Horizontale Ausrichtung des Texts im Label
            valign='middle'  # Vertikale Ausrichtung des Texts im Label
        )

        # Funktion zur Aktualisierung der Größe des Labels nach dem Setzen des Textes
        self.label.bind(texture_size=lambda instance, value: setattr(instance, 'height', instance.texture_size[1]))

        # Erstellen eines ScrollView-Widgets
        scroll_view = ScrollView(size_hint=(1, None), size=(350, self.label.height + 2))

        # Hinzufügen des Labels zum ScrollView
        scroll_view.add_widget(self.label)
        self.root.ids.aktions_leiste.add_widget(scroll_view)

        # "Vorschau" Button hinzufügen
        self.preview_button = Button(text='Life Kamera\n(braucht ein paar Sek. zum Laden)', on_release=self.preview_objectDetection, background_color=(1, 1, 1, 0.5))
        self.root.ids.aktions_leiste.add_widget(self.preview_button)

        # "Anwenden" Button hinzufügen
        self.apply_button = Button(text='Nur Bild', on_release=self.apply_objectDetection, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)
        

    def preview_objectDetection(self, callBackWidget):
        object_detection()

    def apply_objectDetection(self, callBackWidget):
        object_detection(self.actualImagePath)
        self.root.ids.image_widget.source = self.actualImagePath
        self.root.ids.image_widget.reload()
#endregion "Objekt Erkennung"
        

#region "MetaData"
        
    def show_meta_data_controls(self):
        self.clear_action_bar()

        # "Print Exif" Button hinzufügen
        self.apply_button = Button(text='Exif Metadaten', on_release=self.print_exif_data, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)

        # "Print Basic" Button hinzufügen
        self.apply_button = Button(text='Basic Metadaten', on_release=self.print_basic_properties, background_color=(0.486, 0.988, 0, 1))
        self.root.ids.aktions_leiste.add_widget(self.apply_button)

        # "Remove Exif" Button hinzufügen
        self.remove_meta_data_button = Button(text='Exif Metadaten entfernen', on_release=self.remove_meta_data, background_color=(1, 0.5, 0.5, 1))
        self.root.ids.aktions_leiste.add_widget(self.remove_meta_data_button)
    
    def print_basic_properties(self, callBackWidget):
        meta_data = ImageMetaData(self.actualImagePath)
        basic_properties = meta_data.get_basic_properties()

        print(f"Basic Properties für das Bild: {os.path.basename(self.actualImagePath)}\n")
        print("--------------------------------------------------------")
        # durch das tuple basic_properties iterieren
        for i in range(len(basic_properties)):
            print(f"{basic_properties[i]}")
        print("--------------------------------------------------------")

        # Erstellt ein Label, um die Metadaten in einer Tabelle anzuzeigen
        label = Label()
        label.text += "--------------------------------------------------------\n"
        for i in range(len(basic_properties)):
            label.text += f"{basic_properties[i]}\n"
        label.text += "--------------------------------------------------------\n"
        label.text_size = (600, None) # Setzt die Breite für den Textumbruch, Höhe ist unbegrenzt
        label.halign = "center"

        # Erstellt Buttons um Meta-Daten zu löschen oder Popup zu schließen
        button_close = Button(text="Schließen", size_hint=(0.25, 0.15), on_release=self.dismiss_popup)
        button_close.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # BoxLayout mit vertikaler Ausrichtung
        box_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=600)
        # Füge das Label und den Button zur BoxLayout hinzu
        box_layout.add_widget(label)     
        box_layout.add_widget(button_close)

        # Erstelle die ScrollView mit dem BoxLayout als Inhalt
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(box_layout)
    
        # Create the Popup with the ScrollView as its content
        self.meta_data_popup = Popup(title=f"Basic-MetaDaten für das Bild: {os.path.basename(self.actualImagePath)}", content=scroll_view, size_hint=(0.6, 0.8))
        self.meta_data_popup.open()
    
    def dismiss_popup(self, instance):
        self.meta_data_popup.dismiss()

    def print_exif_data(self, callBackWidget):
        meta_data = ImageMetaData(self.actualImagePath)
        exif_data = meta_data.get_exif_values()

        print(f"Exif-MetaDaten für das Bild: {os.path.basename(self.actualImagePath)}\n")
        print("--------------------------------------------------------")
        if not exif_data or not isinstance(exif_data, dict):
            print("Keine Exif-Daten gefunden!")
        else:
            for key, value in exif_data.items():
                print(f"{key}: {value}")
        print("--------------------------------------------------------")

        # Erstellt ein Label, um die Metadaten in einer Tabelle anzuzeigen
        label = Label()
        label.text += "--------------------------------------------------------\n"

        if not exif_data or not isinstance(exif_data, dict):
            label.text += "Keine Exif-Daten gefunden!\n"
        else:
            for key, value in exif_data.items():
                label.text += f"{key}: {value}\n"

        label.text += "--------------------------------------------------------\n"
        label.text_size = (600, None)  # Setzt die Breite für den Textumbruch, Höhe ist unbegrenzt
        label.halign = "center"

        # Erstellt Buttons um Meta-Daten zu löschen oder Popup zu schließen
        button_close = Button(text="Schließen", size_hint=(0.25, 0.15), on_release=self.dismiss_popup)
        button_close.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # BoxLayout mit vertikaler Ausrichtung
        box_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=600)
        # Füge das Label und den Button zur BoxLayout hinzu
        box_layout.add_widget(label)     
        box_layout.add_widget(button_close)

        # Erstelle die ScrollView mit dem BoxLayout als Inhalt
        scroll_view = ScrollView(size_hint=(1, 1))
        scroll_view.add_widget(box_layout)
    
        # Create the Popup with the ScrollView as its content
        self.meta_data_popup = Popup(title=f"Exif-MetaDaten für das Bild: {os.path.basename(self.actualImagePath)}", content=scroll_view, size_hint=(0.6, 0.8))
        self.meta_data_popup.open()

    def remove_meta_data(self, callBackWidget):
        meta_data = ImageMetaData(self.actualImagePath)
        meta_data.delete_EXIF_metadata()

#endregion "MetaData"


if __name__ == '__main__':
    PicTransform().run()

#endregion Main
