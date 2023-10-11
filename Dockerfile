FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
CMD gunicorn --workers=4 --bind 0.0.0.0:8000 src.main:app