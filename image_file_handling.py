import numpy as np
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
        while True:
            try:
                raw_image.seek( frame_counter )
                current_frame = np.array(raw_image)
                image_stack = np.dstack((image_stack, current_frame))
                frame_counter += 1
            except EOFError:
                break
  
    return image_stack
    


