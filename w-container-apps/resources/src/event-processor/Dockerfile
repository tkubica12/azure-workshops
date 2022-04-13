FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt app.py ./
RUN pip3 install -r requirements.txt

CMD [ "python3", "app.py" , "--host=0.0.0.0"]
EXPOSE 5001