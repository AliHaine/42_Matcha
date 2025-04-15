FROM node:23-slim AS build

COPY . /app
WORKDIR /app

RUN npm install
RUN npm run build

FROM nginx:1.27-alpine-slim
COPY --from=build /app/dist/my-app/browser /usr/share/nginx/html