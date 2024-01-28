from PIL import Image, ImageEnhance

# Die Funktion ermöglicht die Anpassung der Sättigung eines Bildes.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das bearbeitet werden soll.
# - saturation_factor: Der Faktor, um den die Sättigung verändert wird (Standardwert ist 1.0, keine Änderung).
# - preview: Gibt an, ob eine Vorschau des bearbeiteten Bildes angezeigt werden soll (Standardwert ist True).
def saettigung(image_path, saturation_factor=1.0, preview=True):
    try:
        # Parameter-Validierung
        if not isinstance(image_path, str):
            raise TypeError("Der Dateipfad zum Bild muss eine Zeichenkette (String) sein.")
        
        if not isinstance(saturation_factor, (int, float)):
            raise TypeError("Der Sättigungsfaktor muss eine Zahl sein.")
        
        if not isinstance(preview, bool):
            raise TypeError("Der Vorschau-Parameter muss ein boolscher Wert sein.")

        # Sinnvoller Input-Check
        if saturation_factor < 0 or saturation_factor > 2:
            raise ValueError("Der Sättigungsfaktor muss im Bereich von 0 bis 2 liegen.")

        # Öffnet das Bild mit dem angegebenen Dateipfad.
        img = Image.open(image_path)
    except Exception as e:
        # Falls ein Fehler beim Öffnen des Bildes oder bei der Validierung auftritt, gibt eine Fehlermeldung aus und beendet die Funktion.
        print(f"Fehler beim Öffnen des Bildes oder ungültige Parameter: {e}")
        return

    # Ändert die Sättigung des Bildes gemäß dem angegebenen Faktor.
    enhanced_img = ImageEnhance.Color(img).enhance(saturation_factor)

    # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
    # oder das bearbeitete Bild wird gespeichert.
    if preview:
        print("Sättigung Preview getriggert")
        enhanced_img.show()
    else:
        print("Sättigung apply getriggert")
        enhanced_img.save(image_path)

    # Gibt eine Erfolgsmeldung mit dem Pfad des bearbeiteten Bildes und dem angewendeten Sättigungsfaktor zurück.
    return image_path + " gesättigt mit einem Faktor von " + str(saturation_factor) + " Prozent"
