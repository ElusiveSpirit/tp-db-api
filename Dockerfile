FROM tiangolo/uwsgi-nginx-flask:flask-python3.5-upload

# Install app dependencies
COPY requirements.txt /conf/requirements.txt
RUN pip install -r /conf/requirements.txt

# Bundle app source
COPY main.py /app/main.py
COPY config.py /app/config.py
COPY app /app/app

