FROM node:22-slim AS build

COPY . /app
WORKDIR /app

RUN npm install
RUN npm run build

FROM nginx:1.25-alpine
COPY --from=build /app/dist/my-app/browser /usr/share/nginx/html
