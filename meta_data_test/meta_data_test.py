import sys
import os
from ImageMetaData_Module import ImageMetaData



def test_basic_metadata_webp():
    print("Aktuelles Arbeitsverzeichnis:", os.getcwd())

    image = ImageMetaData("meta_data_test/testimage_01.webp")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('WEBP', (1024, 1024), 'RGB')
    assert image.has_exif() == False
"""     assert image.get_exif_attributes_of_image() == []
 """
def test_basic_metadata_jpg():
    print("Aktuelles Arbeitsverzeichnis:", os.getcwd())

    image = ImageMetaData("meta_data_test/Canon_40D.jpg")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('JPEG', (100, 77), 'RGB')
    assert image.has_exif() == True

    exif_metadata = image.get_exif_values()
    assert exif_metadata["orientation"] == 1
    assert exif_metadata["x_resolution"] == 300.0
    assert exif_metadata["y_resolution"] == 300.0