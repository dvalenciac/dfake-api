"""
Test API Module
"""
import pytest
import base64
import io
import os
from PIL import Image
from httpx import AsyncClient

SERVICE_URL = os.environ.get("SERVICE_URL")
TOKEN=os.environ.get("CONN_TOKEN").strip()

TEST_IMG = 'test/img/IMG_20240329_131211031.jpg'

HEALTH_EP = "/"
RELOAD_EP = "/reload/"
PREDICT_EP = "/predict_image/"
PREDICT_HM_EP = "/generate_heatmap/"
TIMEOUT = 30

@pytest.mark.asyncio
async def test_API_health():
    """
    Test API health
    """
    url = HEALTH_EP
    async with AsyncClient(base_url=SERVICE_URL, timeout=TIMEOUT) as ac:
        response = await ac.get(url) 
        assert response.status_code == 200
        json_result = response.json()
        assert json_result['API'] == 'OK'

@pytest.mark.asyncio
async def test_reload():
    """
    Test Reload model
    """
    url = RELOAD_EP
    async with AsyncClient(base_url=SERVICE_URL, timeout=TIMEOUT) as ac:
        headers = {'token': TOKEN}
        response = await ac.post(url, headers=headers)
        assert response.status_code == 200
        json_result = response.json()
        assert json_result['API'] == 'OK'

@pytest.mark.asyncio
async def test_predict():
    """
    Test Predict
    """
    url = PREDICT_EP
    async with AsyncClient(base_url=SERVICE_URL, timeout=TIMEOUT) as ac:
        headers = {'token': TOKEN}
        files = {'file': open(TEST_IMG, 'rb')}

        response = await ac.post(url, files=files, headers=headers) 
        assert response.status_code == 200
        json_result = response.json()
        assert json_result['predict_value'] <= 1.0
        assert json_result['fake_real'] in ["FAKE", "REAL"]

@pytest.mark.asyncio
async def test_predict_hm():
    """
    Test Predict Heat MAP
    """
    url = PREDICT_HM_EP
    async with AsyncClient(base_url=SERVICE_URL, timeout=TIMEOUT) as ac:
        headers = {'token': TOKEN}
        files = {'file': open(TEST_IMG, 'rb')}

        response = await ac.post(url, files=files, headers=headers) 
        assert response.status_code == 200
        json_result = response.json()
        assert json_result['predict_value'] <= 1.0
        assert json_result['fake_real'] in ["FAKE", "REAL"]


        img_data = base64.b64decode(json_result['image_resized'])
        img = Image.open(io.BytesIO(img_data))
        img.save('image_resized.png')

        img_data = base64.b64decode(json_result['heatmap'])
        img_hm = Image.open(io.BytesIO(img_data))
        img_hm.save('heatmap.png')
        
