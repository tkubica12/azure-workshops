import redis
import base64
import json
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
import os
from redis.cluster import RedisCluster
from redis import Redis

load_dotenv()

scope = "https://redis.azure.com/.default" 
cluster_mode = os.environ["REDIS_CLUSTER_MODE"]
if cluster_mode == "oss":
    host = os.environ["REDIS_OSS_HOST"]
elif cluster_mode == "enterprise":
    host = os.environ["REDIS_ENTERPRISE_HOST"]
elif cluster_mode == "geo":
    host = os.environ["REDIS_GEO_PRIMARY_HOST"]
port = os.environ["REDIS_PORT"]

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

print("Setting key")
r.set("demo:{shard1}:key1", "value1")

print("Getting key")
t = r.get("demo:{shard1}:key1")
print(f"Got {t}")
