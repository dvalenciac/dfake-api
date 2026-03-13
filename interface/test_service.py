"""
Test an URL
"""
import sys
import os
from httpx import AsyncClient
import asyncio

SERVICE_URL = os.environ.get("SERVICE_URL")
TOKEN=os.environ.get("CONN_TOKEN").strip()

HEALTH_EP = "/"
RELOAD_EP = "/reload/"
PREDICT_EP = "/predict_image/"
PREDICT_HM_EP = "/generate_heatmap/"
TIMEOUT = 30


async def predict(image_path):
    """
    Test Predict
    """
    url = PREDICT_EP
    async with AsyncClient(base_url=SERVICE_URL, timeout=TIMEOUT) as ac:
        headers = {'token': TOKEN}
        files = {'file': open(image_path, 'rb')}
        response = await ac.post(url, files=files, headers=headers) 
        json_result = response.json()
        print(json_result)
        return json_result



if __name__ == '__main__':
    image_path = sys.argv[1]

    if os.path.exists(image_path):
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        file_extension = os.path.splitext(image_path)[1].lower()
            
            # Validate file type
        if file_extension in allowed_extensions:                
            print(f"\n{image_path}")
            result = asyncio.run(predict(image_path))
            print(f"✅ === > {result}\n")
    else:
         print("\n File not found\n")