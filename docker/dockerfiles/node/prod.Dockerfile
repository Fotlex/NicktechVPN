FROM node:22-alpine AS builder

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build


FROM nginx:stable-alpine

COPY --from=builder /app/dist /usr/share/nginx/html

COPY docker/nginx/prod.conf /etc/nginx/templates/default.conf.template

COPY docker/nginx/scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]