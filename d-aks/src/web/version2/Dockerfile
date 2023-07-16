FROM ubuntu:22.04

RUN apt update && apt install -y stress-ng

COPY web2 /usr/local/bin/web2

RUN chmod +x /usr/local/bin/web2

EXPOSE 3000

CMD ["/usr/local/bin/web2"] 