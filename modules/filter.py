# Bild mit Farbfiltern anpassen

'''
Beschreibung der Funktion:
Mit dieser Funktion können vordefinierte Bildfilter auf ein importiertes Bild angewendet werden.
Parameter:
    - name: Der Name des Filters (String).
    - contrast: Der Kontrastwert des Filters (Standardwert ist 1.0).
    - brightness: Der Helligkeitswert des Filters (Standardwert ist 1.0).
    - saturation: Der Sättigungswert des Filters (Standardwert ist 1.0).
    - color_temperature_change: Die Änderung der Farbtemperatur des Filters in Grad (Standardwert ist 0).
    - color_thresholds: Ein 4-Tupel, das die Farbschwellen für die Filterung angibt (Standardwert ist (0, 0, 0, 0)).

Die Parameter-Validierung wurde mit Unterstützung von ChatGPT implementiert.
'''

from PIL import Image, ImageEnhance

# Die Klasse Filter ermöglicht es, vordefinierte Filtereinstellungen zu speichern und auf Bilder anzuwenden, 
# wodurch eine flexible Bildbearbeitung ermöglicht wird.
class Filter:

    # __slots__ wird verwendet, um den Speicherverbrauch der Instanzen zu minimieren.
    __slots__ = ["name",
                 "contrast",
                 "brightness",
                 "saturation",
                 "color_temperature_change",
                 "color_thresholds"]

    # Der Konstruktor initialisiert einen Filter mit den gegebenen Parametern oder Standardwerten.
    def __init__(self,
                 name,
                 contrast: float = 1.0,
                 brightness: float = 1.0,
                 saturation: float = 1.0,
                 color_temperature_change: int = 0,
                 color_thresholds: tuple = (0, 0, 0, 0)):

        try:
            # Parameter-Validierung (Unterstützung von ChatGPT)
            if not isinstance(name, str):
                raise TypeError("Ungültiger Parameter. 'name' muss ein String sein.")
            if not isinstance(contrast, (int, float)):
                raise TypeError("Ungültiger Parameter. 'contrast' muss eine Zahl sein.")
            if not isinstance(brightness, (int, float)):
                raise TypeError("Ungültiger Parameter. 'brightness' muss eine Zahl sein.")
            if not isinstance(saturation, (int, float)):
                raise TypeError("Ungültiger Parameter. 'saturation' muss eine Zahl sein.")
            if not isinstance(color_temperature_change, int):
                raise TypeError("Ungültiger Parameter. 'color_temperature_change' muss eine ganze Zahl sein.")
            if not isinstance(color_thresholds, tuple) or len(color_thresholds) != 4:
                raise TypeError("Ungültiger Parameter. 'color_thresholds' muss ein 4-Tupel sein.")

        except TypeError as te:
            # Falls ein Fehler bei der Parameter-Validierung auftritt, gibt eine Fehlermeldung aus.
            print(f"Fehler bei der Initialisierung des Filters: {te}")
            return

        self.name = name
        self.contrast = contrast
        self.brightness = brightness
        self.saturation = saturation
        self.color_temperature_change = color_temperature_change
        self.color_thresholds = color_thresholds

    # Die Methode apply_config wendet die Filter-Konfiguration auf ein Bild an oder zeigt eine Vorschau an.
    # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
    # oder das bearbeitete Bild wird gespeichert.
    def apply_config(self, image_path: str, preview: bool = True) -> None:
        """
        Wendet die Filter-Konfiguration an oder öffnet ein Vorschau-Fenster.
        """

        try:
            image = Image.open(image_path)
        except:
            # Gibt eine Fehlermeldung aus, wenn das Bild nicht geöffnet werden kann.
            print("Bild konnte nicht geöffnet werden")
            return

        # Hilfsfunktion zum Anwenden von Farbschwellen auf das Bild.
        def apply_threshold(image):
            if (thresh := self.color_thresholds[3]):
                i = image.convert("L").point((lambda x: 255 if x > thresh else 0), mode="1")
                return i.convert("RGB")

            rgb_channels = []

            for channel, threshold in zip(image.split(), self.color_thresholds[0:3]):
                rgb_channels.append(channel.point(lambda x: 255 if x > threshold else 0))

            return Image.merge("RGB", rgb_channels)

        # Hilfsfunktion zum Anpassen der Farbtemperatur des Bildes.
        def adjust_color_temperature(image, r_change=20, b_change=-20):
            r, _, b = image.split()
            r_channel = r.point(lambda x: (x + self.color_temperature_change * r_change))
            b_channel = b.point(lambda x: (x + self.color_temperature_change * b_change))
            return Image.merge("RGB", (r_channel, _, b_channel))

        # Anwenden der Filter auf das Bild entsprechend den Konfigurationsparametern.
        if self.contrast != float(1.0):
            image = ImageEnhance.Contrast(image).enhance(self.contrast)

        if self.brightness != float(1.0):
            image = ImageEnhance.Brightness(image).enhance(self.brightness)

        if self.saturation != float(1.0):
            image = ImageEnhance.Color(image).enhance(self.saturation)

        if self.color_temperature_change != 0:
            image = adjust_color_temperature(image)

        if any(self.color_thresholds) is True:
            image = apply_threshold(image)

        # Entscheidet, ob eine Vorschau des bearbeiteten Bildes angezeigt oder das Bild gespeichert werden soll.
        image.show() if preview else image.save(image_path)

    # Setzt den aktuellen Filter auf den aktuellen Filter.
    def set_current_preset(self):
        Filter_Presets.current_filter = self

    # Gibt den Namen des Filters als Zeichenkette zurück.
    def __str__(self):
        return str(self.name)


class Filter_Presets:

    # Eine Sammlung von vordefinierten Filtereinstellungen als Klassenattribute.
    filter_dict = {
        "Original": Filter("Original"),
        "Grau": Filter("Grau", saturation=0.0),
        "Schwarzweiß": Filter("Schwarzweiß", brightness=1.2, color_thresholds=(0, 0, 0, 175)),
        "Warm": Filter("Warm", color_temperature_change=+2),
        "Kalt": Filter("Kalt", color_temperature_change=-2),
        "Poster": Filter("Poster", brightness=1.0, contrast=1.2, color_thresholds=(170, 170, 170, 0))
    }

    # Das aktuelle Filterobjekt, das auf das Bild angewendet wird.
    current_filter = filter_dict["Original"]
