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
    r = Redis(host=host,
                port=port,
                ssl=True,
                username=user_name,
                password=token.token,
                decode_responses=True)
elif cluster_mode == "oss":
    r = RedisCluster(host=host,
                port=port,
                ssl=True,
                username=user_name,
                password=token.token,
                decode_responses=True)
elif cluster_mode == "geo":
    r = Redis(host=host,
                port=port,
                ssl=True,
                username=user_name,
                password=token.token,
                decode_responses=True)

number_of_shards = 5
keys_per_shard = 5
all_keys = {}
all_key_names = []

# Setting keys on multiple shards using different hash tags
print(f"Setting keys on {number_of_shards} shards with {keys_per_shard} keys each")
for shard in range(1, number_of_shards + 1):
    for key_num in range(1, keys_per_shard + 1):
        key = f"demo{{shard{shard}}}:key{key_num}"
        value = f"shard{shard}-value{key_num}"
        r.set(key, value)
        all_keys[key] = value
        all_key_names.append(key)

# Performing MGET across shards
print("Performing MGET across shards")
values = r.mget(all_key_names)
print(f"MGET returned: {values}")

# Attempting MSET across shards
print("Attempting MSET across shards")
try:
    r.mset(all_keys)
    updated_values = r.mget(all_key_names)
    print(f"MSET succeeded, MGET returned: {updated_values}")
except redis.RedisError as e:
    print(f"MSET failed: {e}")