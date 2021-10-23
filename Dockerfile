# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /showcase
COPY requirements.txt /showcase/
RUN pip install -r requirements.txt
COPY . /showcase/
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]