import logging
from PIL import Image

logging.basicConfig(filename='pictransform.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')


def get_basic_properties(relative_image_path):
    logging.info(f"In function get_imagesize")
    try:
        image = Image.open(relative_image_path)
        logging.info(f"get_basic_properties: relative_image_path: {relative_image_path}")

        image_properties = (image.format, image.size, image.mode)
        logging.info(f"get_basic_properties: image_properties: {image_properties}")

        return image.format, image.size, image.mode
    except FileNotFoundError:
        logging.error("get_basic_properties: Datei nicht gefunden")
        return "Datei nicht gefunden"
    except IOError:
        logging.error("get_basic_properties: Datei konnte nicht geöffnet werden")
        return "Datei konnte nicht geöffnet werden"
    except Exception as error:
        logging.error(f"get_basic_properties: Ein unerwarteter Fehler ist aufgetreten: {error}")
        return f"Ein unerwarteter Fehler ist aufgetreten: {error}"
    

        

