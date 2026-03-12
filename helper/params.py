"""
Global parameters 
"""
import os
from pathlib import Path


#Model Input size
IMAGE_SIZE = (256, 256)
RESULTS = ["FAKE", "REAL"]
TRIGGER_VALUE = 0.51

MODEL_TARGET = os.environ.get("MODEL_TARGET")
MODEL_NAME = os.environ.get("MODEL_NAME").strip() if os.environ.get("MODEL_NAME") else ""
LOCAL_MODEL_PATH = os.environ.get("LOCAL_MODEL_PATH").strip() if os.environ.get("LOCAL_MODEL_PATH") else ""

#upload folder
#UPLOAD_DIR = Path("uploads")
#UPLOAD_DIR.mkdir(exist_ok=True)


################## VALIDATIONS #################

env_valid_options = dict(
    MODEL_TARGET=["local", "gcs", "mlflow"],
)

def validate_env_value(env, valid_options):
    """ 
    Validate an environment variable value
    """
    env_value = os.environ[env]
    if env_value not in valid_options:
        raise NameError(f"Invalid value for {env} in `.env` file: {env_value} must be in {valid_options}")


#Loop to validate environment variables 
for env, valid_options in env_valid_options.items():
    validate_env_value(env, valid_options)

