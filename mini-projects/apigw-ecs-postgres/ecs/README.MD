# Local Install Commands

python3 -m venv ./venv
source ./venv/bin/activate 
python3 -m pip install -r requirements.txt
python3 service.py

# Docker Local Running
docker build --tag my-docker-app .
docker images
docker run -d -p 80:80 my-docker-app

# Reference
