FROM python:3.11-slim

# install dependencies
RUN apt update && apt upgrade -y

COPY . /app

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD [ "python", "/app/run.py" ]