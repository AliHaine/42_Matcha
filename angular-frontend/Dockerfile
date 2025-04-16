FROM node:22-alpine AS build

COPY . /app
WORKDIR /app

ENV NODE_OPTIONS="--max-old-space-size=1024"

RUN npm install
RUN npm run build

FROM nginx:1.27-alpine-slim
COPY --from=build /app/dist/my-app/browser /usr/share/nginx/html