from image_file_handling import read_images_to_array 
import os
import pytest
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image
"""

"""

def test_read_images_to_array(tmpdir):
    a = np.random.randint(200, size = (14, 10))
    b = np.random.randint(200, size = (14, 10))
    c = np.random.randint(200, size = (14, 10))
    d = np.array([a,b,c])[0]
    test_stack_data_np = d
    test_stack_data_tiff = Image.fromarray(test_stack_data_np)
    """make temp file to read"""
    path_of_temp = tmpdir.mkdir("sub").join("image_test.tiff")
    test_stack_data_tiff.save(str(path_of_temp))
    assert (read_images_to_array(str(path_of_temp))==test_stack_data_np).all()
    assert read_images_to_array('') == []