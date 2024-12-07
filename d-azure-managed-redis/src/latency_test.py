import redis
import base64
import json
import time
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
from redis.cluster import RedisCluster
from redis import Redis

load_dotenv()

scope = "https://redis.azure.com/.default"  # The current scope is for public preview and may change for GA release.
cluster_mode = os.environ["REDIS_CLUSTER_MODE"]
if cluster_mode == "oss":
    host = os.environ["REDIS_OSS_HOST"]
elif cluster_mode == "enterprise":
    host = os.environ["REDIS_ENTERPRISE_HOST"]
elif cluster_mode == "geo":
    host = os.environ["REDIS_GEO_PRIMARY_HOST"]
port = os.environ["REDIS_PORT"]
iterations = int(os.environ.get("ITERATIONS", 10))  # Number of iterations for latency measurement
number_of_shards = int(os.environ.get("NUMBER_OF_SHARDS", 5))  # Number of shards to test

def extract_username_from_token(token):
    parts = token.split('.')
    base64_str = parts[1]

    if len(base64_str) % 4 == 2:
        base64_str += "=="
    elif len(base64_str) % 4 == 3:
        base64_str += "="

    json_bytes = base64.b64decode(base64_str)
    json_str = json_bytes.decode('utf-8')
    jwt = json.loads(json_str)

    return jwt['oid']

cred = DefaultAzureCredential()
token = cred.get_token(scope)
user_name = extract_username_from_token(token.token)

if cluster_mode == "enterprise":
    r = Redis(host=host, port=port, ssl=True, username=user_name, password=token.token, decode_responses=True)
elif cluster_mode == "oss":
    r = RedisCluster(host=host, port=port, ssl=True, username=user_name, password=token.token, decode_responses=True)
elif cluster_mode == "geo":
    r = Redis(host=host, port=port, ssl=True, username=user_name, password=token.token, decode_responses=True)

write_latencies = []
read_latencies = []

for shard in range(1, number_of_shards + 1):
    for i in range(iterations):
        key = f"demo{{shard{shard}}}:key1"
        
        # Measure write latency
        start_time = time.time()
        r.set(key, "value1")
        write_latencies.append((time.time() - start_time) * 1000) 

        # Measure read latency
        start_time = time.time()
        t = r.get(key)
        read_latencies.append((time.time() - start_time) * 1000) 

avg_write_latency = sum(write_latencies) / (iterations * number_of_shards)
avg_read_latency = sum(read_latencies) / (iterations * number_of_shards)

print(f"Average write latency: {avg_write_latency:.6f} milliseconds")
print(f"Average read latency: {avg_read_latency:.6f} milliseconds")