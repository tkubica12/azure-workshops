FROM ubuntu:22.04

RUN apt update && apt install -y stress-ng

COPY web /usr/local/bin/web

RUN chmod +x /usr/local/bin/web

EXPOSE 3000

CMD ["/usr/local/bin/web"] 