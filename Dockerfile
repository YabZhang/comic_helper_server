FROM python:3.6-jessie

WORKDIR /app
COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ["python", "manage.py", "debugserver"]

