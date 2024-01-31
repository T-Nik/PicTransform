# Fehler Popup-Fenster

'''
Beschreibung der Funktion:
Mit dieser Funktion kann eine Fehlermeldung in einem Popup-Fenster angezeigt werden.
Parameter:
    - message: Die Fehlermeldung, die im Popup-Fenster angezeigt werden soll.

Vergleiche folgende Quelle anhand derer der Code implementiert wurde:
    https://kivy.org/doc/stable/api-kivy.uix.popup.html
'''

# Importiere die Kivy-Bibliothek und die erforderlichen Kivy-Komponenten
import kivy
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# Funktion zum Anzeigen einer Fehlermeldung in einem Popup-Fenster
def show_error_popup(message):

    # Erstelle ein Label für den Popup-Inhalt mit der übergebenen Fehlermeldung
    content = Label(text=message, text_size=(350, None), halign='center', valign='middle')

    # Erstelle ein Popup-Fenster mit dem erstellten Label als Inhalt
    error_popup = Popup(title="Fehler", content=content, size_hint=(None, None), size=(400, 300))

    # Öffne das Popup-Fenster, um die Fehlermeldung anzuzeigen
    error_popup.open()