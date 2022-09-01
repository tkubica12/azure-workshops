FROM python:3.8
RUN mkdir /app
COPY requirements.txt /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD gunicorn -b 0.0.0.0:8080 -c config.py -e PYTHONBUFFERED=TRUE app:app --log-file=-