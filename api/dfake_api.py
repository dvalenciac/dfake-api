#import numpy as np
#import pandas as pd
import sys
import os
import io
import base64
from PIL import Image
from helper import params
from helper.images import resize_image
from helper.registry import load_model, get_response
from keras.preprocessing.image import img_to_array
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.model = None

#TODO check if needed in PROD
# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    """ API Health check 
    """
    if app.model is None:
        app.model =  load_model()
    return {
        'API': 'OK'
    }

@app.post("/reload/")
def reload(request: Request):
    """ API Reload model 
    """
    headers = request.headers
    token = headers.get("token")
    # If there is no token or it does not match --> Error
    if params.TOKEN != token:
        return JSONResponse(
                    status_code=400,
                    content={
                        "ERROR":  "Misisng or wrong token."  
                    }
                )
    
    app.model =  load_model()
    if app.model is None:
            return JSONResponse(
                    status_code=500,
                    content={
                        "ERROR":  "Error loading model."  
                    }
                )
    else:
        return {
            'API': 'OK'
        }

@app.post("/predict_image/")
async def predict(file: UploadFile = File(...),
                  request: Request=None):
    """
    Upload an image file(acepted types: '.jpg', '.jpeg', '.png', '.gif', '.bmp')  
        return :
            "fake_real":  FAKE or REAL
            "predict_value": A probability between 0 and 1 that it's a Fake image (1 = FAKE, 0 = REAL) 
    """
    headers = request.headers
    token = headers.get("token")
    # If there is no token or it does not match --> Error
    if params.TOKEN != token:
        return JSONResponse(
                    status_code=400,
                    content={
                        "ERROR":  "Misisng or wrong token."  
                    }
                )
    
    if app.model is None:
        app.model =  load_model()
        if app.model is None:
            return JSONResponse(
                    status_code=500,
                    content={
                        "ERROR":  "Error loading model."  
                    }
                )
    try:
        if file.content_type is not None:
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="File must be an image")
        else:
            # If content_type is None, check by file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            # Validate file type
            if file_extension not in allowed_extensions:
                raise HTTPException(status_code=400, detail="File must be an image")
        contents = file.file
        image = Image.open(contents)
        #image processed 
        processed_image = resize_image(image)

        X_pred = img_to_array(processed_image)
    
        shape = X_pred.shape
        if shape != params.IMAGE_SIZE + (3,):
            return JSONResponse(
                status_code=400,
                content={
                    "ERROR":  "The image size is not as expected.",
                    "expected": params.IMAGE_SIZE + (3,), 
                    "received": shape,                
                }
            )
        shape = (-1,) + shape
        
        X_pred = X_pred.reshape(shape)
        y_pred = app.model.predict(X_pred)
        
        content = get_response(y_pred)
        return JSONResponse(
            status_code=200,
            content=content
        )
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@app.post("/generate_heatmap/")
async def predict_heatmap(file: UploadFile = File(...),
                  request: Request=None):
    """
    Upload an image file(acepted types: '.jpg', '.jpeg', '.png', '.gif', '.bmp')  
        return :
            "fake_real":  FAKE or REAL
            "predict_value": A probability between 0 and 1 that it's a Fake image (1 = FAKE, 0 = REAL) 
            "image_resized":  The original image, resized to 256x256,
            "heatmap": A heatmap image, resized to 256x256,            
    """
    headers = request.headers
    token = headers.get("token")
    # If there is no token or it does not match --> Error
    if params.TOKEN != token:
        return JSONResponse(
                    status_code=400,
                    content={
                        "ERROR":  "Misisng or wrong token."  
                    }
                )
    
    if app.model is None:
        app.model =  load_model()
        if app.model is None:
            return JSONResponse(
                    status_code=500,
                    content={
                        "ERROR":  "Error loading model."  
                    }
                )
    try:
        if file.content_type is not None:
            if not file.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="File must be an image")
        else:
            # If content_type is None, check by file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
            file_extension = os.path.splitext(file.filename)[1].lower()
            
            # Validate file type
            if file_extension not in allowed_extensions:
                raise HTTPException(status_code=400, detail="File must be an image")
        
        contents = file.file
        image = Image.open(contents)
        #image processed 
        processed_image = resize_image(image)

        X_pred = img_to_array(processed_image)
    
        shape = X_pred.shape
        if shape != params.IMAGE_SIZE + (3,):
            return JSONResponse(
                status_code=400,
                content={
                    "ERROR":  "The image size is not as expected.",
                    "expected": params.IMAGE_SIZE + (3,), 
                    "received": shape,                
                }
            )
        shape = (-1,) + shape
        
        X_pred = X_pred.reshape(shape)
        y_pred = app.model.predict(X_pred)
        
        #heat map
        # Open image with PIL
        heatmap_img = processed_image
        
        # Convert to numpy array for processing
        #img_array = np.array(img)

        # Modify image (example: convert to grayscale)
        if heatmap_img.mode != 'L':
            img_processed = heatmap_img.convert('L')
        else:
            img_processed = heatmap_img

        # Encode image as base64
        #converts images to bytes 
        img_byte_arr = io.BytesIO()
        processed_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()      
        img_proc_base64 = base64.b64encode(img_byte_arr).decode('utf-8')

        img_byte_arr = io.BytesIO()
        img_processed.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        heatmap_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        
        content = get_response(y_pred)

        content["image_resized"] = img_proc_base64
        content["heatmap"] = heatmap_base64
        return JSONResponse(
            status_code=200,
            content=content
        )
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()