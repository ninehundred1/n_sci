import numpy as np
import sqlite3
import glob
import os
try:
    from PIL import Image
except ImportError:
    import Image

__all__ = ['read_images','read_images_stack']

def read_images_to_array(filename):
    """ Wrapper around pillow image load. will read the tiff stack of images and return numpy array
    :param path: string of file name
    :returns: numpy array, if no tiff supplied, array will be empty
    """
    image_stack = []
    if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
        frame_counter = 1
        raw_image = Image.open(filename)
        image_stack = np.array(raw_image)
        frames_to_add = True
        while frames_to_add:
            try:
                raw_image.seek( frame_counter )
                current_frame = np.array(raw_image)
                image_stack = np.dstack((image_stack, current_frame))
                frame_counter += 1
            except EOFError:
                frames_to_add = False
    return image_stack

def write_image_array_to_file(array, save_path):
    try:
        pil_image = Image.fromarray(array)
        pil_image.save(str(save_path))
        return True
    except IOError:
        return False

def write_frames_to_sqlite(filename, data_base_name):
    conn = sqlite3.connect(data_base_name)
    conn.execute('''create table if not exists images (
                        path unique not null, 
                        image blob
                    )''')
    if filename.lower().endswith('.tif') or filename.lower().endswith('.tiff'):
        frame_counter = 0
        raw_image = Image.open(filename)
        frames_to_add = True
        with conn:
            while frames_to_add:
                try:
                    current_frame = np.array(raw_image)
                    #conn.execute('INSERT INTO {name} (data) values(?, ?)', current_frame, format(name = data_base_name) )
                    conn.execute("INSERT INTO {tn} ({idf}) values(?, ?), current_frame"\
                        .format(tn=data_base_name, idf='data'))
                    frame_counter += 1
                    raw_image.seek( frame_counter )
                except EOFError:
                    frames_to_add = False

               

