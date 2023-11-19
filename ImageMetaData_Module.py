import logging
from PIL import Image
import exif

from ImageErrorHandling_Module import ImageErrorHandling

#logging.basicConfig(filename='pictransform.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

class ImageMetaData:
    def __init__(self, relative_filepath):
        # Setup logger 
        self.logger = logging.getLogger(__name__)

        # Setup attributes
        self.relative_filepath = relative_filepath
        self.attr_basic_properties = self.__get_basic_properties()
        if self.__exif_supported_format() and self.__has_exif():
            self.attr_has_exif = self.__has_exif()
            self.exif_attributes = self.__get_exif_attributes()
        else:
            self.attr_has_exif = False
            self.exif_attributes = []


    # Accessing the attributes
    def get_basic_properties(self):
        return self.attr_basic_properties
    
    def has_exif(self):
        return self.attr_has_exif
    
    def get_exif_attributes(self):
        return self.exif_attributes
    
    

    # Helping methods
    def __get_basic_properties(self):
        self.logger.info("method: get_basic_properties")
        try:
            with Image.open(self.relative_filepath) as image:
                basic_properties = (image.format, image.size, image.mode)
                self.logger.info(f"get_basic_properties: relative_filepath: {self.relative_filepath}")
                self.logger.info(f"get_basic_properties: basic_properties: {basic_properties}")
                return basic_properties
        except Exception as error:
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)



    ## EXIF
    def __exif_supported_format(self):
        self.logger.info("method: exif_supported_format")
        return self.get_basic_properties()[0] in ('TIFF', 'JPEG')
    


    def __has_exif(self):
        self.logger.info("method: has_exif")
        if not self.__exif_supported_format():
            return False
        try:
            with open(self.relative_filepath, 'rb') as image_file:
                image = exif.Image(image_file)
                return image.has_exif
        except Exception as error:
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)



    def __get_exif_attributes(self):
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
            ImageErrorHandling.handle_error(self.logger, error, self.relative_filepath)
