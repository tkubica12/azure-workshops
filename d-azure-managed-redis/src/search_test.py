import redis
import base64
import json
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import os
from redis.cluster import RedisCluster
from redis import Redis
from openai import AzureOpenAI
import struct

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

# Connect Azure OpenAI Embeddings model
azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_openai_embeddings_model = os.getenv("AZURE_OPENAI_EMBEDDINGS_MODEL")

token_provider = get_bearer_token_provider(
    cred, "https://cognitiveservices.azure.com/.default"
)

azure_openai_client = AzureOpenAI(
  azure_ad_token_provider=token_provider,
  api_version = "2024-09-01-preview",
  azure_endpoint = azure_openai_endpoint
)

# Prepare texts for search
texts = [
    "The quick brown fox jumps over the lazy dog. This is a well-known pangram used in typography. It contains every letter of the English alphabet. It's often used to display font samples.",
    "Artificial intelligence is transforming the world. From healthcare to finance, AI is making a significant impact. It's revolutionizing the way we live and work. The future of AI is full of possibilities.",
    "Python is a versatile programming language. It's widely used in web development, data science, and automation. Python's simplicity and readability make it a popular choice. It's a great language for beginners and experts alike.",
    "The sun rises in the east and sets in the west. This is a fundamental fact of our planet's rotation. It's a predictable pattern that governs our day and night cycle. The beauty of a sunrise or sunset is universally appreciated.",
    "Climate change is a pressing global issue. It's caused by human activities like deforestation and burning fossil fuels. The effects are widespread and severe, impacting weather patterns and sea levels. Addressing climate change requires collective action.",
    "The internet has revolutionized communication. It's made the world more connected than ever before. Information is now at our fingertips. However, it also raises concerns about privacy and security.",
    "Space exploration has always fascinated humanity. The idea of discovering the unknown is thrilling. With advancements in technology, we're exploring further than ever before. The possibility of life on other planets is an intriguing question.",
    "Machine learning is a subset of artificial intelligence. It involves training algorithms to learn from data. Machine learning is used in various applications like image recognition and predictive analytics. It's a rapidly growing field with immense potential.",
    "The human brain is a complex organ. It's the control center of the body, responsible for thoughts and actions. Despite advances in neuroscience, much about the brain remains a mystery. Understanding the brain is one of science's greatest challenges.",
    "The Great Wall of China is a historical marvel. It's one of the Seven Wonders of the Medieval World. The wall was built to protect against invasions. Today, it's a popular tourist attraction and a symbol of China's rich history.",
    "Electric vehicles are gaining popularity. They're seen as a solution to reduce carbon emissions. With advancements in battery technology, EVs are becoming more efficient. The shift to electric mobility is a step towards a sustainable future.",
    "Quantum computing is an exciting frontier in technology. It leverages the principles of quantum mechanics. Quantum computers have the potential to solve complex problems faster than classical computers. This technology could revolutionize various industries.",
    "The ocean covers more than 70% of the Earth's surface. It's home to a diverse range of marine life. The ocean plays a crucial role in regulating the climate. Protecting the ocean is vital for maintaining the planet's health.",
    "Blockchain technology underpins cryptocurrencies like Bitcoin. It's a decentralized ledger that records transactions across a network of computers. Blockchain is praised for its security and transparency. It's being explored for use in various sectors beyond finance.",
    "The human genome project was a landmark scientific endeavor. It aimed to map all the genes in the human genome. The project was completed in 2003, providing a wealth of genetic information. This knowledge is transforming medicine and biotechnology.",
    "Renewable energy sources are key to a sustainable future. Solar, wind, and hydroelectric power are clean alternatives to fossil fuels. Investing in renewable energy can reduce greenhouse gas emissions. It's an essential step in combating climate change.",
    "Virtual reality creates immersive digital experiences. It's used in gaming, education, and training simulations. VR has the potential to change the way we interact with digital content. The technology is becoming more accessible and advanced.",
    "The theory of evolution explains the diversity of life on Earth. It's a fundamental concept in biology. Evolutionary theory is supported by a vast amount of evidence from various scientific disciplines. It provides a framework for understanding the natural world.",
    "Cybersecurity is a critical concern in the digital age. As technology advances, so do the methods of cyberattacks. Protecting sensitive information is paramount. Cybersecurity measures are essential to safeguard against data breaches and cyber threats.",
    "The arts play a significant role in human culture. They allow for expression and creativity. Art can take many forms, including music, literature, and visual arts. It's a reflection of society and can inspire change."
]

search_text = "I want to know about electronic money that is not traditional fiat currency"
search_keyword = "Bitcoins"

# Create index for RedisSearch
index_name = "text_idx"
try:
    r.ft(index_name).dropindex(delete_documents=True)
except:
    pass

schema = (
    TextField("text"),
    VectorField("vector", "FLAT", {"TYPE": "FLOAT32", "DIM": 3072, "DISTANCE_METRIC": "COSINE"})
)

r.ft(index_name).create_index(schema, definition=IndexDefinition(prefix=["doc:"], index_type=IndexType.HASH))

# Add documents to the index
print("\n\n****** Adding documents to the index ******")
for i, text in enumerate(texts):
    key = f"doc:{{shard1}}:{i}"
    if r.exists(key) == 0:
        embedding = azure_openai_client.embeddings.create(input=[text], model=azure_openai_embeddings_model).data[0].embedding
        vector = struct.pack(f'{len(embedding)}f', *embedding)
        r.hset(key, mapping={"text": text, "vector": vector})
        print(f"Added document {text[:20]}.. to index.")
    else:
        print(f"Document {text[:20]}.. already exists in the index.")

# Keyword search
print(f"\n\n****** Keyword search for '{search_keyword}' ******")
query = Query(f"@text:{search_keyword}")
results = r.ft(index_name).search(query)
print(f"Keyword search results for '{search_keyword}':")
for doc in results.docs:
    print(doc.text)

# Vector search (Placeholder, as actual vector search requires vector embeddings)
print(f"\n\n****** Vector search for '{search_text}' ******")
embedding = azure_openai_client.embeddings.create(input=[search_text], model=azure_openai_embeddings_model).data[0].embedding
vector = struct.pack(f'{len(embedding)}f', *embedding)
query = Query("*=>[KNN 1 @vector $vec AS score]").sort_by("score").paging(0, 5).return_fields("text", "score").dialect(2)
params = {"vec": vector}
results = r.ft(index_name).search(query, query_params=params)
print(f"Vector search results for '{search_text}':")
for doc in results.docs:
    print(doc.text, doc.score)