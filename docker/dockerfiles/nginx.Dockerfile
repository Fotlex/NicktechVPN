FROM nginx:stable-alpine

COPY ./nginx/prod.conf.template /etc/nginx/templates/default.conf.template

COPY --from=frontend /app/dist /usr/share/nginx/html

CMD ["/bin/sh", "-c", "envsubst < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]