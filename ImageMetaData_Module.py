import logging
from PIL import Image
import exif
import json 

from ImageErrorHandling_Module import ImageErrorHandling

#logging.basicConfig(filename='pictransform.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

class ImageMetaData:
    def __init__(self, relative_filepath):
        # Initialisiert den Logger für diese Klasse
        self.logger = logging.getLogger(__name__)

        # Setzt die Attribute der Klasse: Dateipfad und grundlegende Eigenschaften des Bildes
        self.relative_filepath = relative_filepath



    # Getter-Methoden
    def get_basic_properties(self):
        # Gibt die grundlegenden Eigenschaften des Bildes zurück
        return self.__get_basic_properties()
    
    def has_exif(self):
        # Gibt zurück, ob das Bild EXIF-Attribute hat
        return self.__has_exif()
    
    def get_exif_values(self):
        # Gibt die EXIF-Attribute des Bildes zurück
        if self.__exif_supported_format() and self.__has_exif():
            return json.loads(json.dumps(self.__get_exif_attributes_and_values_of_image()))
        else:
            return []
    
    def delete_EXIF_metadata(self):
        self.__remove_exif_and_overwrite(self)
        return self.get_exif_values(self)

    


    # Hilfsmethoden
    def __get_basic_properties(self):
        # Protokolliert den Aufruf der Methode und versucht, die grundlegenden Eigenschaften des Bildes zu ermitteln
        self.logger.info("method: __get_basic_properties")
        try:
            with Image.open(self.relative_filepath) as image:
                # Öffnet das Bild und extrahiert Format, Größe und Modus (Farbsarstellung RGB, RGBA, ...)
                basic_properties = (image.format, image.size, image.mode)
                self.logger.info(f"__get_basic_properties: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"__get_basic_properties: basic_properties: {basic_properties}")
                return basic_properties
        except Exception as error:
            # Fehlerbehandlung im Falle eines Fehlers beim Öffnen des Bildes
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    ## EXIF
    def __exif_supported_format(self):
        # Überprüft, ob das Bildformat EXIF-Informationen unterstützen kann
        self.logger.info("method: __exif_supported_format")
        return self.get_basic_properties()[0] in ('TIFF', 'JPEG')

    def __has_exif(self):
        # Überprüft, ob das Bild EXIF-Informationen enthält
        self.logger.info("method: __has_exif")
        if not self.__exif_supported_format():
            return False
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                return image.has_exif
        except Exception as error:
            # Fehlerbehandlung, falls ein Fehler beim Zugriff auf die EXIF-Informationen auftritt
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    def __get_exif_attributes_and_values_of_image(self):
        # Liest und gibt die EXIF-Attribute und Werte des Bildes zurück
        self.logger.info("method: __get_exif_attributes_and_values_of_image")
        if not self.__exif_supported_format():
            return "Format not supported"
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                exif_properties = image.get_all()
                self.logger.info(f"__get_exif_attributes_and_values_of_image: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"__get_exif_attributes_and_values_of_image: basic_properties: {exif_properties}")
                return exif_properties
        except Exception as error:
            # Fehlerbehandlung, falls ein Fehler beim Lesen der EXIF-Attribute auftritt
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)


    def __remove_exif_and_overwrite(self):
        # Entfernt EXIF-Metadaten aus dem Bild und überschreibt das Originalbild.
   
        self.logger.info("method: __remove_exif_and_overwrite")
        if self.has_exif():
            try:
                # Bild ohne EXIF-Daten öffnen
                with Image.open(self.relative_filepath) as img:
                    data = img.getdata()

                    # Neues Bild ohne EXIF-Daten erstellen
                    new_img = Image.new(img.mode, img.size)
                    new_img.putdata(data)

                    # Bild am gleichen Pfad überschreiben
                    new_img.save(self.relative_filepath, quality=95, optimize=True)
                    
                    self.logger.info("__remove_exif_and_overwrite: EXIF-Daten entfernt und Bild erfolgreich überschrieben.")

            except Exception as error:
                # Fehlerbehandlung
                ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)
                self.logger.error(f"Fehler beim Entfernen der EXIF-Daten: {error}")