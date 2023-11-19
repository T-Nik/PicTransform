import logging
from PIL import Image


#logging.basicConfig(filename='pictransform.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')


def get_basic_properties(relative_image_path):
    logging.info("In function get_imagesize")
    try:
        with Image.open(relative_image_path) as image:
            logging.info(f"get_basic_properties: relative_image_path: {relative_image_path}")
            return image.format, image.size, image.mode
    except FileNotFoundError:
        logging.error(f"get_basic_properties: Datei nicht gefunden - {relative_image_path}")
        raise FileNotFoundError(f"Datei nicht gefunden - {relative_image_path}")
    except IOError:
        logging.error(f"get_basic_properties: Datei konnte nicht geöffnet werden - {relative_image_path}")
        raise IOError(f"Datei konnte nicht geöffnet werden - {relative_image_path}")
    except Exception as error:
        logging.error(f"get_basic_properties: Ein unerwarteter Fehler ist aufgetreten: {error}")
        raise Exception(f"Ein unerwartener Fehler ist aufgetreten: {error}")


        

