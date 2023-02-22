FROM nginx
COPY startup.sh /docker-entrypoint.d/
RUN sed -i 's/\r$//' /docker-entrypoint.d/startup.sh