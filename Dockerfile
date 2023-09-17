FROM python:3.11
WORKDIR /app
COPY . /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "populate_db"]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]