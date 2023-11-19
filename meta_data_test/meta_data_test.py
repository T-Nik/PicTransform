import sys
sys.path.append('..')

import meta_data

basic_metadata = meta_data.get_basic_properties("testimage_01.webp")

def test_basic_metadata():
    assert basic_metadata == ('WEBP', (1024, 1024), 'RGB')