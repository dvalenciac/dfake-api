#import numpy as np
#import pandas as pd
import sys
import os
import shutil
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

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    """
    Upload an image file and return a probability percentage that it's a Fake image
    """
    try:
        print(file.content_type)
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
        return JSONResponse(
            status_code=200,
            content={
                "result": 0.5,                
            }
        )
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@app.post("/predict-hm/")
async def predict_heatmap(file: UploadFile = File(...)):
    """
    Upload an image file and 
        return :
            * A probability percentage that it's a Fake image
            * The original image, resized to params.IMAGE_SIZE
            * A heatmap image (size = params.IMAGE_SIZE)  
    """
    try:
        print(file.content_type)
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
        return JSONResponse(
            status_code=200,
            content={
                "result": 0.5,                
            }
        )
    
    except Exception as e:
        type, value, traceback = sys.exc_info()
        print(type, value, traceback )
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()