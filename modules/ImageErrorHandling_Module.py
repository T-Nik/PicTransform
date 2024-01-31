# Logging-System

'''
Beschreibung der Funktion:
Mit dieser Funktion wird eine Klasse für ein Logging-System für die Fehlerbehandlung implementiert.
Parameter:
    - logger: Ein Logger-Objekt, das für das Logging von Fehlermeldungen verwendet wird (muss
      ein Objekt der Klasse logging.Logger sein).
    - error: Das aufgetretene Fehlerobjekt, das von der Bildverarbeitung generiert wurde.
    - relative_image_path: Der relative Pfad zum importierten Bild (String).

Die Parameter-Validierung wurde mit Unterstützung von ChatGPT implementiert.
'''

import logging
from modules.logger_config import setup_logging

# Konfiguriert das Logging-System für das gesamte Modul. Die Konfiguration ist in der 'logger_config' definiert.
# Dies ermöglicht eine zentrale Verwaltung der Logging-Einstellungen.
setup_logging()

class ImageErrorHandling:
    # Die Klasse ImageErrorHandling dient als zentrale Stelle für die Fehlerbehandlung im Zusammenhang mit Bildoperationen.
    # Sie nutzt die Kapselung, um die Fehlerbehandlungslogik von der Hauptlogik der Bildverarbeitung zu trennen.

    @staticmethod
    def handle_error(logger, error, relative_image_path):
        try:
            # Parameter-Validierung (Unterstützung von ChatGPT)
            if not isinstance(logger, logging.Logger):
                raise TypeError("Ungültiger Parameter. 'logger' muss ein Logger-Objekt sein.")
            if not isinstance(relative_image_path, str):
                raise TypeError("Ungültiger Parameter. 'relative_image_path' muss ein String sein.")

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

        except Exception as e:
            # Falls ein Fehler bei der Parameter-Validierung auftritt, gibt eine Fehlermeldung aus.
            print(f"Fehler bei der Fehlerbehandlung: {e}")

