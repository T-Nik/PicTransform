from PIL import Image, ImageEnhance

# Die Funktion ermöglicht die Anpassung der Sättigung eines Bildes.
# Parameter:
# - image_path: Der Dateipfad zum Bild, das bearbeitet werden soll.
# - saturation_factor: Der Faktor, um den die Sättigung verändert wird (Standardwert ist 1.0, keine Änderung).
# - preview: Gibt an, ob eine Vorschau des bearbeiteten Bildes angezeigt werden soll (Standardwert ist True).
def saettigung(image_path, saturation_factor=1.0, preview=True):
    try:
        # Öffnet das Bild mit dem angegebenen Dateipfad.
        img = Image.open(image_path)
    except:
        # Falls ein Fehler beim Öffnen des Bildes auftritt, gibt eine Fehlermeldung aus und beendet die Funktion.
        print("Fehler beim Öffnen des Bildes")
        return

    # Ändert die Sättigung des Bildes gemäß dem angegebenen Faktor.
    enhanced_img = ImageEnhance.Color(img).enhance(saturation_factor)

    # Es wird entweder eine Vorschau des bearbeiteten Bildes angezeigt und eine entsprechende Meldung zurückgegeben, 
    # oder das bearbeitete Bild wird gespeichert, und eine Erfolgsmeldung mit dem Pfad und dem Radius wird zurückgegeben.
    if preview:
        # Wenn Vorschau gewünscht ist, gibt eine Meldung aus und zeigt die Vorschau an.
        print("Sättigung Preview getriggert")
        enhanced_img.show()
    else:
        # Wenn Vorschau nicht gewünscht ist, gibt eine Meldung aus und speichert das bearbeitete Bild.
        print("Sättigung apply getriggert")
        enhanced_img.save(image_path)

    # Gibt eine Erfolgsmeldung mit dem Pfad des bearbeiteten Bildes und dem angewendeten Sättigungsfaktor zurück.
    return image_path + " gesättigt mit einem Faktor von " + str(saturation_factor) + " Prozent"
