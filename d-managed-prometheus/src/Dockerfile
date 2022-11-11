FROM python 
COPY . /app/
RUN cd /app && pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "/app/counter.py"]