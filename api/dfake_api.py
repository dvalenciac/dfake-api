#import numpy as np
#import pandas as pd
import sys
import os
import shutil
import io
import base64
from PIL import Image
from helper import params
from fastapi import FastAPI, File, UploadFile, HTTPException
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
    return {
        'API': 'OK'
    }

@app.post("/predict_image/")
async def predict(file: UploadFile = File(...)):
    """
    Upload an image file and return a probability percentage that it's a Fake image
    """
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
        
        # Create file path
        file_path = params.UPLOAD_DIR / file.filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # "filename": file.filename,
        #         "content_type": file.content_type,
        #         "file_size": file_path.stat().st_size
        predict_value = 0.51
        fake_real = params.RESULTS[0]
        return JSONResponse(
            status_code=200,
            content={
                "fake_real":  fake_real,
                "predict_value": predict_value,                
            }
        )
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@app.post("/generate_heatmap/")
async def predict_heatmap(file: UploadFile = File(...)):
    """
    Upload an image file and 
        return :
            * A probability percentage that it's a Fake image
            * The original image, resized to params.IMAGE_SIZE
            * A heatmap image (size = params.IMAGE_SIZE)  
    """
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
        
        # Create file path
        file_path = params.UPLOAD_DIR / file.filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Open image with PIL
        #TODO get the real image
        test_response = "test/img/00A0WLZE5X.jpg"
        img = Image.open(test_response)
        
        # Convert to numpy array for processing
        #img_array = np.array(img)

        # Modify image (example: convert to grayscale)
        if img.mode != 'L':
            img_processed = img.convert('L')
        else:
            img_processed = img

        # Save processed image to bytes
        img_byte_arr = io.BytesIO()
        img_processed.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Encode image as base64
        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
        predict_value = 0.51
        fake_real = params.RESULTS[0]
        return {
            "fake_real":  fake_real,
            "predict_value": predict_value,
            "image_resized": img_base64,
            "heatmap": img_base64,
        }
        
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()