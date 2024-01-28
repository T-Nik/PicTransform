import logging
from PicTransform.modules.logger_config import setup_logging

# Konfiguriert das Logging-System für das gesamte Modul. Die Konfiguration ist in der 'logger_config' definiert.
# Dies ermöglicht eine zentrale Verwaltung der Logging-Einstellungen.
setup_logging()

class ImageErrorHandling:
    # Die Klasse ImageErrorHandling dient als zentrale Stelle für die Fehlerbehandlung im Zusammenhang mit Bildoperationen.
    # Sie nutzt die Kapselung, um die Fehlerbehandlungslogik von der Hauptlogik der Bildverarbeitung zu trennen.

    @staticmethod
    def handle_error(logger, error, relative_image_path):
        # Eine statische Methode, die zur Behandlung von Fehlern aufgerufen wird. 
        # Sie benötigt keinen Zugriff auf Instanzvariablen oder -methoden, daher ist sie als statische Methode definiert.
        # Parameter: 
        # - logger: Das Logger-Objekt, das zum Protokollieren von Fehlern verwendet wird.
        # - error: Das aufgetretene Fehlerobjekt.
        # - relative_image_path: Der Pfad des betroffenen Bildes, um spezifischere Fehlermeldungen zu ermöglichen.

        if isinstance(error, FileNotFoundError):
            # Behandelt den Fall, wenn die Bild-Datei nicht gefunden wird.
            logger.error(f"Datei nicht gefunden - {relative_image_path}")
            # Löst eine FileNotFoundException aus, um dem aufrufenden Code mitzuteilen, dass das Bild nicht gefunden wurde.
            raise FileNotFoundError(f"Datei nicht gefunden - {relative_image_path}")

        elif isinstance(error, IOError):
            # Behandelt Fehler beim Zugriff auf die Datei (z.B. Lese-/Schreibfehler).
            logger.error(f"Datei konnte nicht geöffnet werden - {relative_image_path}")
            # Löst eine IOError aus, um anzugeben, dass ein Fehler beim Öffnen der Datei aufgetreten ist.
            raise IOError(f"Datei konnte nicht geöffnet werden - {relative_image_path}")

        else:
            # Behandelt alle anderen Arten von Fehlern.
            logger.error(f"Ein unerwarteter Fehler ist aufgetreten: {error}")
            # Löst eine allgemeine Exception aus, um einen unerwarteten Fehler anzuzeigen.
            raise Exception(f"Ein unerwarteter Fehler ist aufgetreten: {error}")
