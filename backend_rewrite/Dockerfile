FROM python:3.13-alpine

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD [ "python", "-u", "/app/run.py" ]