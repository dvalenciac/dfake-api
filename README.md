# dfake-api
API Deep Images Project

Python Version 3.12.9


# There is no model file in the project 
# !!!!! ** Please download it from this link ** !!!!!!!!
https://drive.google.com/file/d/1MEnryqykEt2wMdebAsvZpyGoNHgVdGec/view

# put the file in this folder, if you change the name or the location change the env variable LOCAL_MODEL_PATH 
dfake-api/model/baseline.joblib


# The API version 0.0.2 let create the docker image 
To run it use this command:

docker run -p 8000:8000 --env-file .env  dfake-api


!! Atention!!
The .env has changed use the model .env.sample