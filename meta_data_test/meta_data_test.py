import sys
sys.path.append('..')

import meta_data

basic_metadata = meta_data.get_basic_properties("testimage_01.jpg")

def test_format():
    assert basic_metadata == ('WEBP', (1024, 1024), 'RGB')