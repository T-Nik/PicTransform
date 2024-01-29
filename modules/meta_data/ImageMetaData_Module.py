import logging
from PIL import Image
import exif
import json
from modules.ImageErrorHandling_Module import ImageErrorHandling

# Konfiguration des Logging-Systems für bessere Fehlernachverfolgung
logging.basicConfig(format='%(asctime)s %(message)s')

class ImageMetaData:
    def __init__(self, relative_filepath):
        # Initialisiert die Klasse. Jede Instanz der Klasse arbeitet mit einem spezifischen Bild, dessen Pfad hier übergeben wird.
        self.logger = logging.getLogger(__name__)  # Erstellt einen Logger speziell für diese Klasse.

        # Parameter-Validierung für relative_filepath
        if not isinstance(relative_filepath, str):
            raise TypeError("Ungültiger Parameter. 'relative_filepath' muss ein String sein.")
        
        self.relative_filepath = relative_filepath  # Speichert den relativen Pfad zur Bilddatei.

    # Öffentliche Methoden (Teil der Schnittstelle zur Außenwelt):
    # Diese Methoden definieren, wie andere Teile des Programms oder andere Programme mit dieser Klasse interagieren können.
    # Sie kapseln die interne Logik der Klasse und bieten eine klare und verständliche API.

    def get_basic_properties(self):
        # Bietet eine öffentliche Methode, um grundlegende Eigenschaften des Bildes abzurufen.
        return self.__get_basic_properties()
    
    def has_exif(self):
        # Bietet eine öffentliche Methode, um zu überprüfen, ob das Bild EXIF-Daten enthält.
        return self.__has_exif()

    def get_exif_values(self):
        # Bietet eine öffentliche Methode, um EXIF-Informationen des Bildes zu extrahieren.
        if self.__exif_supported_format() and self.__has_exif():
            try:
                return json.loads(json.dumps(self.__get_exif_attributes_and_values_of_image()))
            except (TypeError, ValueError):
                return []
        else:
            return []

    def delete_EXIF_metadata(self):
        # Bietet eine öffentliche Methode, um EXIF-Daten aus dem Bild zu entfernen.
        self.__remove_exif_and_overwrite()
        return self.get_exif_values()

    # Private Methoden (Interne Implementierungsdetails):
    # Diese Methoden sind nur innerhalb der Klasse sichtbar und werden verwendet, um die Funktionalität zu implementieren,
    # die von den öffentlichen Methoden bereitgestellt wird. Durch die Trennung dieser Details wird die Komplexität für
    # den Benutzer der Klasse reduziert und die interne Logik geschützt.

    def __get_basic_properties(self):
        # Interne Methode zur Ermittlung grundlegender Bildeigenschaften.
        self.logger.info("method: __get_basic_properties")
        try:
            with Image.open(self.relative_filepath) as image:
                basic_properties = (image.format, image.size, image.mode)
                self.logger.info(f"__get_basic_properties: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"__get_basic_properties: basic_properties: {basic_properties}")
                return basic_properties
        except Exception as error:
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    def __exif_supported_format(self):
        # Interne Überprüfung, ob das Bildformat EXIF-Informationen unterstützt.
        self.logger.info("method: __exif_supported_format")
        return self.get_basic_properties()[0] in ('TIFF', 'JPEG')

    def __has_exif(self):
        # Interne Methode zur Überprüfung der EXIF-Verfügbarkeit im Bild.
        self.logger.info("method: __has_exif")
        if not self.__exif_supported_format():
            return False
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                return image.has_exif
        except Exception as error:
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    def __get_exif_attributes_and_values_of_image(self):
        # Interne Methode zum Abrufen von EXIF-Attributen und deren Werten.
        self.logger.info("method: __get_exif_attributes_and_values_of_image")
        if not self.__exif_supported_format():
            return []
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                exif_properties = image.get_all()
                self.logger.info(f"__get_exif_attributes_and_values_of_image: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"__get_exif_attributes_and_values_of_image: basic_properties: {exif_properties}")
                return exif_properties
        except Exception as error:
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    def __remove_exif_and_overwrite(self):
        # Interne Methode zum Entfernen von EXIF-Daten und Überschreiben des Bildes.
        self.logger.info("method: __remove_exif_and_overwrite")
        if self.has_exif():
            try:
                with Image.open(self.relative_filepath) as img:
                    data = img.getdata()
                    new_img = Image.new(img.mode, img.size)
                    new_img.putdata(data)
                    new_img.save(self.relative_filepath, quality=95, optimize=True)
                    self.logger.info("__remove_exif_and_overwrite: EXIF-Daten entfernt und Bild erfolgreich überschrieben.")
            except Exception as error:
                ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)
                self.logger.error(f"Fehler beim Entfernen der EXIF-Daten: {error}")
