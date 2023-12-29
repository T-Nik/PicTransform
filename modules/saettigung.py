from PIL import Image, ImageEnhance


def saettigung(image_path, saturation_factor=1.0, preview=True):
    try:
        img = Image.open(image_path)
    except:
        print("Fehler beim Öffnen des Bildes")
        return

    # Sättigung ändern
    enhanced_img = ImageEnhance.Color(img).enhance(saturation_factor)

    # Bild anzeigen lassen oder speichern
    if preview:
        print("Sättigung Preview getriggert")
        enhanced_img.show()
    else:
        # Speichern des Bildes
        print("Sättigung apply getriggert")
        enhanced_img.save(image_path)

    return image_path + " gesättigt mit einem Faktor von" + str(saturation_factor) + "Prozent"
