"""
Test API Module
"""
import pytest
import requests


# Basic upload
URL = "http://localhost:8000/predict/"
files = {'file': open('../img/IMG_20240329_131211031.jpg', 'rb')}
response = requests.post(URL, files=files, timeout=30)
print(response.json())

