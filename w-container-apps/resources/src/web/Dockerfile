FROM nginx
COPY src/ /usr/share/nginx/html/
COPY version /
COPY startup.sh /docker-entrypoint.d/
RUN sed -i 's/\r$//' /docker-entrypoint.d/startup.sh