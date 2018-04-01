FROM python:3.6-slim

WORKDIR /course

ADD . /course

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "--host", "0.0.0.0"]
