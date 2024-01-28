import logging
# Importiert das Logging-Modul, um ein Logging-System für die Anwendung bereitzustellen.


def setup_logging():
    # Definiert eine Funktion zum Einrichten der grundlegenden Konfiguration des Logging-Systems.
    # Diese Funktion wird aufgerufen, um das Logging-System zu initialisieren und zu konfigurieren.

    # 'basicConfig' ist eine Methode im Logging-Modul, die die grundlegenden Einstellungen für das Logging-System festlegt.
    # Hier wird das Format der Log-Nachrichten und das Log-Level bestimmt.
    # - '%(asctime)s': Fügt den Zeitstempel hinzu, wann die Log-Nachricht erstellt wurde.
    # - '%(name)s': Der Name des Loggers, der die Nachricht erzeugt hat.
    # - '%(levelname)s': Der Schweregrad der Nachricht (INFO, WARNING, ERROR, etc.).
    # - '%(message)s': Die eigentliche Log-Nachricht.
    # - 'level=logging.INFO': Setzt das Log-Level auf INFO, was bedeutet, dass INFO-, WARNING-, ERROR- und CRITICAL-Meldungen protokolliert werden.
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
