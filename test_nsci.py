from image_file_handling import read_images_to_array 
from image_file_handling import write_image_array_to_file 
from image_file_handling import write_frames_to_sqlite
import os
import pytest
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image
"""
pytest for all the functions
"""

def create_sample_np_arrays():
    """ 
    :returns a 3d np stack of 3 frames and a 2d np array of 1 frame
    """
    frame_1 = np.random.randint(200, size = (14, 10))
    frame_2 = np.random.randint(200, size = (14, 10))
    frame_3 = np.random.randint(200, size = (14, 10))
    test_stack_data_np = np.array([frame_1, frame_3, frame_3])[0]
    return test_stack_data_np, frame_1

@pytest.mark.order1
def test_read_images_to_array(tmpdir):
    """ pytest read_images_to_array
    :param tmpdir generates a temp directory for a mock data file to be saved first
    test1: same 3d stack gets returned from load that was saved
    test2: same 2d array get returned 
    test3: empyt file returns correctly an empty array
    """
    np_stack, np_array = create_sample_np_arrays()
    test_stack_data_pil = Image.fromarray(np_stack)
    test_single_image_pil = Image.fromarray(np_array)
    temp_path = tmpdir.mkdir("sub")
    path_of_temp_stack = temp_path.join("stack_test.tiff")
    path_of_temp_image = temp_path.join("image_test.tiff")
    test_stack_data_pil.save(str(path_of_temp_stack))
    test_single_image_pil.save(str(path_of_temp_image))
    #test much match all entries
    assert (read_images_to_array(str(path_of_temp_stack)) == np_stack).all()
    assert (read_images_to_array(str(path_of_temp_image)) == np_array).all()
    assert read_images_to_array('') == []
    print 'LOG: test_read_images_to_array - passed'

@pytest.mark.order2
def test_write_image_array_to_file(tmpdir):
    """ pytest test_write_image_array_to_file
    :param tmpdir generates a temp directory for a mock data file to be saved
    test1: same 3d array can be loaded that was saved
    test2: same 2d array can be loaded that was saved
    load is assumed to be functional if test reaches here
    """
    np_stack, np_array = create_sample_np_arrays()
    temp_path = tmpdir.mkdir("sub")
    path_of_temp_stack = temp_path.join("stack_test.tiff")
    path_of_temp_image = temp_path.join("image_test.tiff")
    write_image_array_to_file(np_stack, path_of_temp_stack)
    write_image_array_to_file(np_array, path_of_temp_image)
    assert (read_images_to_array(str(path_of_temp_stack)) == np_stack).all()
    assert (read_images_to_array(str(path_of_temp_image)) == np_array).all()
    print 'LOG: test_write_image_array_to_file - passed'

@pytest.mark.order3
def test_write_frames_to_sqlite(tmpdir):
    np_stack, np_array = create_sample_np_arrays()
    test_stack_data_pil = Image.fromarray(np_stack)
    test_single_image_pil = Image.fromarray(np_array)
    temp_path = tmpdir.mkdir("sub")
    path_of_temp_stack = temp_path.join("stack_test.tiff")
    path_of_temp_image = temp_path.join("image_test.tiff")
    test_stack_data_pil.save(str(path_of_temp_stack))
    test_single_image_pil.save(str(path_of_temp_image))
    assert (write_frames_to_sqlite(str(path_of_temp_stack),'pytest.db') == np_stack).all()
    assert (write_frames_to_sqlite(str(path_of_temp_image),'pytest.db') == np_array).all()
    assert write_frames_to_sqlite('') == []
    print 'LOG: test_read_images_to_array - passed'