"""
Resize an image to a fix (params.IMAGE_SIZE ) size 
"""
from params import IMAGE_SIZE
from skimage import io, img_as_ubyte, transform


def resize_image(image_path):

    # Read image
    image = io.imread(image_path)

    # Resize image
    resized_image = transform.resize(image, IMAGE_SIZE)

     # Save image (needs to convert back to uint8 if necessary)
    io.imsave(f'{resized_image}', img_as_ubyte(resized_image))
    return resized_image
   


