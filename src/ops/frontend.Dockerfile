FROM nginx
COPY ./docker-provision/nginx.conf  /etc/nginx/
EXPOSE 80

