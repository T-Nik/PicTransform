import sys
sys.path.append('..')
from ImageMetaData_Module import ImageMetaData


import meta_data_basic


def test_basic_metadata():
    image = ImageMetaData("testimage_01.webp")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('WEBP', (1024, 1024), 'RGB')

def test_basic_metadata():
    image = ImageMetaData("Canon_40D.jpg")
    basic_metadata = image.get_basic_properties()
    assert basic_metadata == ('JPEG', (100, 77), 'RGB')

def test_exif_metadata_format_not_supported():
    image = ImageMetaData("testimage_01.webp")
    exif_metadata = image.has_exif()
    assert exif_metadata == "Format not supported"

def test_exif_metadata_format_supported():
    image = ImageMetaData("Canon_40D.jpg")
    exif_metadata = image.has_exif()
    assert exif_metadata == True

def test_exif_attributes():
    image = ImageMetaData("Canon_40D.jpg")
    exif_metadata = image.get_exif_attributes()
    assert exif_metadata == ['orientation', 'x_resolution', 'y_resolution', 'resolution_unit', 'software', 'datetime', '_exif_ifd_pointer', 'compression', 'jpeg_interchange_format', 'jpeg_interchange_format_length', 'color_space', 'pixel_x_dimension', 'pixel_y_dimension']
