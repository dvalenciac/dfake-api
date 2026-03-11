FROM python:3.12-slim

COPY api /dfake-api/api
COPY helper /dfake-api/helper
COPY /model/baseline.joblib /dfake-api/model/baseline.joblib 

COPY setup.py  /dfake-api/setup.py 
COPY requirements.txt /dfake-api/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /dfake-api/requirements.txt

CMD uvicorn dfake-api.api.dfake_api:app --host 0.0.0.0