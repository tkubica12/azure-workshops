from prometheus_client import start_http_server, Counter
import random
import time

if __name__ == '__main__':
    c = Counter('my_failures', 'Description of counter')
    start_http_server(8000)
    while True:
        c.inc(random.randrange(1,20,1))
        time.sleep(random.randrange(1,5,1))