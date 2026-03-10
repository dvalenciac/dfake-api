"""
Resize an image to a fix (params.IMAGE_SIZE ) size 
"""
from helper.params import IMAGE_SIZE
from PIL import Image

def resize_image(imafile: Image):
    """
    Converts an image of size (N,M) to an image of size IMAGE_SIZE 
    """
    # Read image
    # Resize image
    resized_image = imafile.resize(IMAGE_SIZE)
    return resized_image

