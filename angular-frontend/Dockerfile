FROM node:22-slim

COPY . /app
WORKDIR /app

RUN npm install

CMD [ "npx", "ng", "serve", "--host", "0.0.0.0", "--port", "4200" ]