from helper.registry import load_model
from helper.params import IMAGE_SIZE
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array


def pred(image = None) -> float:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    if image is None:
        image = Image.open("image_resized.png")
    
    X_pred = img_to_array(image)
    
    shape = X_pred.shape
    shape = (-1,) + shape
    X_pred = X_pred.reshape(shape)

    model = load_model()
    assert model is not None

    y_pred = model.predict(X_pred)

    print("\n✅ prediction done: ", y_pred, y_pred.shape, "\n")
    return y_pred.item(0)


if __name__ == '__main__':
    print("\n✅ test prediction= ", pred(), "\n")
    