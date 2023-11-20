import logging
from PIL import Image
import exif

from ImageErrorHandling_Module import ImageErrorHandling

#logging.basicConfig(filename='pictransform.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

class ImageMetaData:
    def __init__(self, relative_filepath):
        # Initialisiert den Logger für diese Klasse
        self.logger = logging.getLogger(__name__)

        # Setzt die Attribute der Klasse: Dateipfad und grundlegende Eigenschaften des Bildes
        self.relative_filepath = relative_filepath
        self.attr_basic_properties = self.__get_basic_properties()
        
        # Prüft, ob das Bildformat EXIF-Informationen unterstützt und ob solche vorhanden sind
        if self.__exif_supported_format() and self.__has_exif():
            self.attr_has_exif = self.__has_exif()
            self.attr_exif_attributes_of_image = self.__get_exif_attributes_of_image()
        else:
            # Setzt die EXIF-Attribute auf False bzw. eine leere Liste, falls nicht unterstützt oder nicht vorhanden
            self.attr_has_exif = False
            self.attr_exif_attributes_of_image = []

    # Getter-Methoden
    def get_basic_properties(self):
        # Gibt die grundlegenden Eigenschaften des Bildes zurück
        return self.attr_basic_properties
    
    def has_exif(self):
        # Gibt zurück, ob das Bild EXIF-Attribute hat
        return self.attr_has_exif
    
    def get_exif_attributes_of_image(self):
        # Gibt die EXIF-Attribute des Bildes zurück
        return self.attr_exif_attributes_of_image
    
    def get_supported_exif_attributes(self):
        # Listet alle unterstützten EXIF-Attribute auf
        return ['_exif_ifd_pointer', '_gps_ifd_pointer', 'aperture_value', 'brightness_value', 'color_space',
 'components_configuration', 'compression', 'datetime', 'datetime_digitized', 'datetime_original', 'exif_version',
 'exposure_bias_value', 'exposure_mode', 'exposure_program', 'exposure_time', 'f_number', 'flash',
 'flashpix_version', 'focal_length', 'focal_length_in_35mm_film', 'gps_altitude', 'gps_altitude_ref',
 'gps_datestamp', 'gps_dest_bearing', 'gps_dest_bearing_ref', 'gps_horizontal_positioning_error',
 'gps_img_direction', 'gps_img_direction_ref', 'gps_latitude', 'gps_latitude_ref', 'gps_longitude',
 'gps_longitude_ref', 'gps_speed', 'gps_speed_ref', 'gps_timestamp', 'jpeg_interchange_format',
 'jpeg_interchange_format_length', 'lens_make', 'lens_model', 'lens_specification', 'make', 'maker_note',
 'metering_mode', 'model', 'orientation', 'photographic_sensitivity', 'pixel_x_dimension', 'pixel_y_dimension',
 'resolution_unit', 'scene_capture_type', 'scene_type', 'sensing_method', 'shutter_speed_value', 'software',
 'subject_area', 'subsec_time_digitized', 'subsec_time_original', 'white_balance', 'x_resolution',
 'y_and_c_positioning', 'y_resolution']

    # Hilfsmethoden
    def __get_basic_properties(self):
        # Protokolliert den Aufruf der Methode und versucht, die grundlegenden Eigenschaften des Bildes zu ermitteln
        self.logger.info("method: get_basic_properties")
        try:
            with Image.open(self.relative_filepath) as image:
                # Öffnet das Bild und extrahiert Format, Größe und Modus
                basic_properties = (image.format, image.size, image.mode)
                self.logger.info(f"get_basic_properties: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"get_basic_properties: basic_properties: {basic_properties}")
                return basic_properties
        except Exception as error:
            # Fehlerbehandlung im Falle eines Fehlers beim Öffnen des Bildes
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    ## EXIF
    def __exif_supported_format(self):
        # Überprüft, ob das Bildformat EXIF-Informationen unterstützen kann
        self.logger.info("method: exif_supported_format")
        return self.get_basic_properties()[0] in ('TIFF', 'JPEG')

    def __has_exif(self):
        # Überprüft, ob das Bild EXIF-Informationen enthält
        self.logger.info("method: has_exif")
        if not self.__exif_supported_format():
            return False
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                return image.has_exif
        except Exception as error:
            # Fehlerbehandlung, falls ein Fehler beim Zugriff auf die EXIF-Informationen auftritt
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)

    def __get_exif_attributes_of_image(self):
        # Liest und gibt die EXIF-Attribute des Bildes zurück
        self.logger.info("method: get_exif_properties")
        if not self.__exif_supported_format():
            return "Format not supported"
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                exif_properties = image.list_all()
                self.logger.info(f"get_exif_properties: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"get_exif_properties: basic_properties: {exif_properties}")
                return exif_properties
        except Exception as error:
            # Fehlerbehandlung, falls ein Fehler beim Lesen der EXIF-Attribute auftritt
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)
