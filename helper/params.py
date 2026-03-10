"""
Global parameters 
"""

from pathlib import Path


#Model Input size
IMAGE_SIZE = (256, 256)

#upload folder
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
