FROM python:3.12-slim

COPY api /api
COPY helper /helper
COPY /model/baseline.joblib /model/baseline.joblib 

COPY setup.py  /setup.py 
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

CMD uvicorn api.dfake_api:app --host 0.0.0.0