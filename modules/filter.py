from PIL import Image, ImageEnhance

# Die Klasse Filter repräsentiert einen Bildfilter mit einstellbaren Parametern.
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
                 color_thresholds: tuple = (0, 0, 0, 0)):  # RGBW

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

        # Setzt den aktuellen Filter auf den aktuellen Filter.
        self.set_current_preset()

        try:
            image = Image.open(image_path)
        except:
            # Gibt eine Fehlermeldung aus, wenn das Bild nicht geöffnet werden kann.
            print("Bild konnte nicht geöffnet werden")
            return

        # Hilfsfunktion zum Anwenden von Farbschwellen auf das Bild.
        def apply_threshold(image):

            # Wenn ein Schwellenwert für Transparenz gegeben ist, wendet ihn auf das Bild an.
            if (thresh := self.color_thresholds[3]):
                i = image.convert("L").point((lambda x: 255 if x > thresh else 0), mode="1")
                return i.convert("RGB")

            # Andernfalls werden Schwellenwerte für die RGB-Kanäle angewendet.
            rgb_channels = []

            for channel, threshold in zip(image.split(), self.color_thresholds[0:3]):
                rgb_channels.append(channel.point(lambda x: 255 if x > threshold else 0))

            return Image.merge("RGB", rgb_channels)

        # Hilfsfunktion zum Anpassen der Farbtemperatur des Bildes.
        def adjust_color_temperature(image, r_change=20, b_change=-20):

            r, _, b = image.split()

            # Passt die Farbtemperatur durch Änderung der Rot- und Blaukanäle an.
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

# Die Klasse Filter_Presets enthält vordefinierte Filtereinstellungen als Klassenattribute.
class Filter_Presets:

    filter_dict = {
        "Original": Filter("Original"),
        "Grau": Filter("Grau", saturation=0.0),
        "Schwarzweiß": Filter("Schwarzweiß", brightness=1.2, color_thresholds=(0, 0, 0, 175)),
        "Warm": Filter("Warm", color_temperature_change=+2),
        "Kalt": Filter("Kalt", color_temperature_change=-2),
        "Poster": Filter("Poster", brightness=1.0, contrast=1.2, color_thresholds=(170, 170, 170, 0))
    }

    current_filter = filter_dict["Original"]
