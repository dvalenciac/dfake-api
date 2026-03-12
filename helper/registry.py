""""
Helper module that contains the load_model and predict functions 
"""
from helper.params import MODEL_TARGET, LOCAL_MODEL_PATH
from helper.params import MODEL_NAME, TRIGGER_VALUE, RESULTS
import os
from colorama import Fore, Style
import numpy as np
from tensorflow import keras
from joblib import load

def load_model(stage="Production") -> keras.Model:
    """
    Return a saved model:
    - locally (latest one in alphabetical order)
    - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
    - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

    Return None (but do not Raise) if no model is found

    """
    if MODEL_TARGET == "local":
        print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

        # Get the latest model version name by the timestamp on disk

        local_model = MODEL_NAME if MODEL_NAME else ""
        model_path = LOCAL_MODEL_PATH if LOCAL_MODEL_PATH else ""
        local_model = os.path.join(model_path, local_model)

        if not local_model:
            return None


        print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

        latest_model = load(local_model)

        print("✅ Model loaded from local disk")

        return latest_model

    # elif MODEL_TARGET == "gcs":
    #     # 🎁 We give you this piece of code as a gift. Please read it carefully! Add a breakpoint if needed!
    #     print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

    #     client = storage.Client()
    #     blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))

    #     try:
    #         latest_blob = max(blobs, key=lambda x: x.updated)
    #         latest_model_path_to_save = os.path.join(LOCAL_MODEL_PATH, latest_blob.name)
    #         latest_blob.download_to_filename(latest_model_path_to_save)

    #         latest_model = keras.models.load_model(latest_model_path_to_save)

    #         print("✅ Latest model downloaded from cloud storage")

    #         return latest_model
    #     except:
    #         print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")

    #         return None

    # elif MODEL_TARGET == "mlflow":
    #     print(Fore.BLUE + f"\nLoad [{stage}] model from MLflow..." + Style.RESET_ALL)

    #     # Load model from MLflow
    #     model = None
    #     mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    #     client = MlflowClient()

    #     try:
    #         model_versions = client.get_latest_versions(name=MLFLOW_MODEL_NAME, stages=[stage])
    #         model_uri = model_versions[0].source

    #         assert model_uri is not None
    #     except:
    #         print(f"\n❌ No model found with name {MLFLOW_MODEL_NAME} in stage {stage}")

    #         return None

    #     model = mlflow.tensorflow.load_model(model_uri=model_uri)

    #     print("✅ Model loaded from MLflow")
    #     return model
    # else:
    #     return None


def get_response(y_predict: np.ndarray):
    """
    Returns a dictionary with the values, including the meaning of the higher percentage   
    """
    predict_value = y_predict.item(0)
    if predict_value > TRIGGER_VALUE:
        fake_real = RESULTS[1]
    else:
        fake_real = RESULTS[0]
    
    content={
                "fake_real":  fake_real,
                "predict_value": predict_value,                
            }
    return content
    