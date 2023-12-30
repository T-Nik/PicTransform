import logging
from modules.meta_data.logger_config import setup_logging

setup_logging()

class ImageErrorHandling:
    @staticmethod
    def handle_error(logger, error, relative_image_path):
        if isinstance(error, FileNotFoundError):
            logger.error(f"Datei nicht gefunden - {relative_image_path}")
            raise FileNotFoundError(f"Datei nicht gefunden - {relative_image_path}")
        elif isinstance(error, IOError):
            logger.error(f"Datei konnte nicht geöffnet werden - {relative_image_path}")
            raise IOError(f"Datei konnte nicht geöffnet werden - {relative_image_path}")
        else:
            logger.error(f"Ein unerwarteter Fehler ist aufgetreten: {error}")
            raise Exception(f"Ein unerwarteter Fehler ist aufgetreten: {error}")
