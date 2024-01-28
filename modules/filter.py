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
                 color_thresholds: tuple = (0, 0, 0, 0)):  # RGBW

        try:
            # Parametervalidierung
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

        except TypeError as e:
            print(f"Ein Fehler bei der Parametervalidierung ist aufgetreten: {e}")
            return

        # Setzt die Parameter
        self.name = name
        self.contrast = contrast
        self.brightness = brightness
        self.saturation = saturation
        self.color_temperature_change = color_temperature_change
        self.color_thresholds = color_thresholds

    # Restlicher Code bleibt unverändert
    def apply_config(self, image_path: str, preview: bool = True) -> None:
        # ...

    def set_current_preset(self):
        # ...

    def __str__(self):
        return str(self.name)

# Restlicher Code bleibt unverändert
