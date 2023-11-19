import sys
sys.path.append('..')
from ImageMetaData_Module import ImageMetaData


def test_basic_metadata_webp():
    image = ImageMetaData("testimage_01.webp")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('WEBP', (1024, 1024), 'RGB')
    assert image.has_exif() == False
    assert image.get_exif_attributes_of_image() == []

def test_basic_metadata_jpg():
    image = ImageMetaData("Canon_40D.jpg")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('JPEG', (100, 77), 'RGB')
    assert image.has_exif() == True

    exif_metadata = image.get_exif_attributes_of_image()
    assert exif_metadata == ['orientation', 'x_resolution', 'y_resolution', 'resolution_unit', 'software', 'datetime', '_exif_ifd_pointer', 'compression', 'jpeg_interchange_format', 'jpeg_interchange_format_length', 'color_space', 'pixel_x_dimension', 'pixel_y_dimension']
